from flask import Blueprint, request, jsonify, url_for, render_template, redirect, session
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from .db import db
from .models import Students
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import create_access_token, create_refresh_token
import os
from datetime import timedelta


bcrypt = Bcrypt()
mail = Mail()
s = URLSafeTimedSerializer(os.environ.get('KEY'))
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template("login.html", error="Username and password are required."), 400

        student = Students.query.filter_by(username=username).first()

        if student:
            if bcrypt.check_password_hash(student.password, password):
                access_token = create_access_token(
                    identity=student.id, expires_delta=timedelta(hours=1))
                session['access_token'] = access_token
                session['student_id'] = student.id
                session['role'] = student.role
                return redirect(url_for('views.index'))
            else:
                return render_template("login.html", error="Incorrect password."), 401
        else:
            return render_template("login.html", error="Username not found."), 404

    except Exception as e:
        return render_template("login.html", error="An unexpected error occurred: " + str(e)), 500


@auth.route('/signup', methods=['POST'])
def signup():
    id = request.form.get('id')
    fullname = request.form.get('fullname')
    gender = request.form.get('gender')
    class_name = request.form.get('class_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400

    if Students.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_student = Students(
        id=id,
        fullname=fullname,
        gender=gender,
        class_name=class_name,
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )

    db.session.add(new_student)
    db.session.commit()

    # Tạo token xác nhận và gửi email
    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    send_welcome_email(email, fullname)
    send_confirmation_email(email, confirm_url)

    return render_template('login.html')


def send_confirmation_email(email, confirm_url):
    msg = Message('Confirm your account', recipients=[email])
    msg.body = f'Please click the following link to confirm your account: {confirm_url}'
    mail.send(msg)


def send_welcome_email(email, fullname):
    msg = Message('Welcome to Our Community!',
                  sender='dutlibrary1301@gmail.com',
                  recipients=[email])
    msg.body = (
        f'Hello {fullname},\n\n'
        'Welcome to our community! We are thrilled to have you join us.\n\n'
        'Feel free to explore our features and don’t hesitate to reach out if you need any assistance.\n\n'
        'To get full access to all our features, please confirm your email address.\n\n'
        'Thank you for joining us! We’re excited to see you in our community.\n\n'
        'Best regards,\n'
    )
    mail.send(msg)


@auth.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        # Try to load the email from the token
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Find the student using the email from the token
    student = Students.query.filter_by(email=email).first()

    if student:
        # Activate the account
        student.is_active = True
        db.session.commit()

        return render_template('mail_confirm_success.html'), 200
    else:
        return jsonify({"error": "Student not found"}), 404


@auth.route('/account/activate/<student_id>', methods=['POST'])
def activate_account(student_id):
    student = Students.query.get_or_404(student_id)

    # Create the confirmation token
    token = s.dumps(student.email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    send_confirmation_email(student.email, confirm_url)

    return redirect(url_for('views.profile', student_id=student.id))


@auth.route('/login-page', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth.route('/signup-page', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    session.pop('student_id', None)
    session.pop('access_token', None)
    return redirect(url_for('views.index'))
