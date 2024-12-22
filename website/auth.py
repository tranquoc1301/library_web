from flask import Blueprint, request, jsonify, url_for, render_template, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from .db import db
from .models import Users
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

        user = Users.query.filter_by(username=username).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(
                    identity=user.id, expires_delta=timedelta(hours=1))
                session['access_token'] = access_token
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect(url_for('views.index'))
            else:
                return render_template("login.html", error="Incorrect password."), 401
        else:
            return render_template("login.html", error="Username not found."), 404

    except Exception as e:
        return render_template("login.html", error="An unexpected error occurred: " + str(e)), 500


@auth.route('/signup', methods=['POST'])
def signup():
    fullname = request.form.get('fullname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    avatar = "avatars/user.png"

    if password != confirm_password:
        flash('Passwords do not match. Please try again.', 'danger')
        return "", 400

    if Users.query.filter_by(email=email).first():
        flash('Email already exists. Please use a different email.', 'danger')
        return "", 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(
        fullname=fullname,
        username=username,
        email=email,
        avatar=avatar,
        password=hashed_password,
        is_active=False
    )

    db.session.add(new_user)
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

    # Find the user using the email from the token
    user = Users.query.filter_by(email=email).first()

    if user:
        # Activate the account
        user.is_active = True
        db.session.commit()

        return render_template('mail_confirm_success.html'), 200
    else:
        return jsonify({"error": "user not found"}), 404


@auth.route('/account/activate/<user_id>', methods=['POST'])
def activate_account(user_id):
    user = Users.query.get_or_404(user_id)

    # Create the confirmation token
    token = s.dumps(user.email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    send_confirmation_email(user.email, confirm_url)

    return redirect(url_for('views.profile', user_id=user.id))


@auth.route('/login-page', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth.route('/signup-page', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # If the request method is GET, render the change password form
    if request.method == 'GET':
        return render_template('change_password.html')

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        new_password_confirm = request.form.get('new_password_confirm')

        # Check if the new password and confirmation match
        if new_password != new_password_confirm:
            flash('Passwords do not match. Please try again.', 'error')
            # Redirect to the previous page if passwords do not match
            return redirect(request.referrer)

        # Hash and save the new password
        hashed_password = bcrypt.generate_password_hash(
            new_password).decode('utf-8')
        # Get the user based on the session's user_id
        user = Users.query.get(session['user_id'])

        if user:
            # If user exists, update the password and commit the change
            user.password = hashed_password
            db.session.commit()
            # Log the user out by removing their user_id from the session
            session.pop('user_id', None)

            # Redirect the user to the login page after successful password change
            return redirect(url_for('auth.login_page'))

        else:
            # If user is not found, display an error and redirect to the previous page
            flash('User not found. Please try again.', 'error')
            # Redirect to the previous page if user is not found
            return redirect(request.referrer)


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('access_token', None)
    return redirect(url_for('views.index'))

# Forgot Password Route


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset')
            reset_url = url_for('auth.reset_password_form',
                                token=token, _external=True)
            send_reset_password_email(email, reset_url)
            flash('Password reset link has been sent to your email.', 'success')
        else:
            flash('If the email is registered, a reset link will be sent.', 'info')
        return redirect(request.referrer)

    return render_template('forgot_password.html')


# Reset Password Form Route (GET)
@auth.route('/reset-password/<token>', methods=['GET'])
def reset_password_form(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except Exception:
        flash("The password reset link is invalid or has expired.", "error")
        return redirect(url_for('auth.forgot_password'))
    return render_template('reset_password.html', token=token)


# Reset Password Submit Route (POST)
@auth.route('/reset-password', methods=['POST'])
def reset_password_submit():
    token = request.form.get('token')
    print(f"Token received: {token}")  # Log the received token

    if not token:
        flash("Token is missing. Please request a new password reset link.", "error")
        return redirect(url_for('auth.forgot_password'))

    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except Exception:
        flash("The password reset link is invalid or has expired.", "error")
        return redirect(url_for('auth.forgot_password'))

    user = Users.query.filter_by(email=email).first()
    if user:
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('new_password_confirm')

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(request.referrer)

        # Hash and save the new password
        user.password = bcrypt.generate_password_hash(new_password)
        db.session.commit()
        flash('Password has been reset successfully. Please log in with your new password.', 'success')
        return redirect(request.referrer)
    else:
        flash('User not found. Please try again.', 'error')
        return redirect(url_for('auth.forgot_password'))

# Send Reset Password Email


def send_reset_password_email(email, reset_url):
    msg = Message('Reset Your Password', recipients=[email])
    msg.body = f'Please click the following secure link to reset your password: {reset_url}'
    mail.send(msg)
