from flask import request, jsonify
from ..db import db
from ..library_ma import StudentSchema
from ..models import Students
from werkzeug.utils import secure_filename
import os

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


def add_student_service(data):
    errors = student_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    try:
        new_student = Students(
            fullname=data['fullname'],
            gender=data['gender'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_student)
        db.session.commit()

        return new_student, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def get_all_students_service():
    all_students = Students.query.all()
    return all_students  # Trả về danh sách đối tượng sinh viên


def get_student_by_id_service(id):
    student = Students.query.get(id)
    if not student:
        return None, 404
    return student  # Trả về đối tượng sinh viên


def update_student_service(id):
    student = Students.query.get(id)
    if not student:
        return None, 404

    data = request.form  # Use form data
    errors = student_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    try:
        for key, value in data.items():
            setattr(student, key, value)

        db.session.commit()
        return student_schema.jsonify(student), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_student_service(id):
    student = Students.query.get(id)
    if not student:
        return None, 404

    try:
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def change_password_service(id, data):
    student = Students.query.get(id)
    if not student:
        return None, 404

    if 'password' not in data or 'confirm_password' not in data:
        return {"error": "Password and confirm password are required."}, 400

    if data['password'] != data['confirm_password']:
        return {"error": "Passwords do not match."}, 400

    try:
        student.password = data['password']
        db.session.commit()
        return student, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_avatar_service(id):
    student = Students.query.get(id)
    if not student:
        return {"error": "Student not found"}, 404

    avatar = request.files.get('avatar')
    if not avatar or avatar.filename == '':
        return {"error": "No file selected."}, 400

    if not allowed_file(avatar.filename):
        return {"error": "Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed."}, 400

    filename = secure_filename(avatar.filename)
    avatar_path = os.path.join('avatars', filename)
    save_path = os.path.join('website', 'static', avatar_path)

    try:
        # Save the avatar image file
        avatar.save(save_path)
        student.avatar = avatar_path.replace(os.sep, '/')
        db.session.commit()

        return {"message": "Avatar uploaded successfully.", "avatar_url": student.avatar}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
