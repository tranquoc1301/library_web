from flask import request, flash
from ..db import db
from ..models import Users
from werkzeug.utils import secure_filename
import os


def add_user_service():
    data = request.form
    errors = []
    if not data.get('fullname') or not data.get('username') or not data.get('email') or not data.get('password'):
        errors.append("All fields are required.")
    if errors:
        return {"errors": errors}, 400

    try:
        new_user = Users(
            fullname=data['fullname'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def get_all_users_service():
    all_users = Users.query.all()
    return all_users


def get_user_by_id_service(id: int):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    return user


def update_user_service(id: int):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    data = request.form  # Use form data
    errors = []
    if 'fullname' not in data or 'username' not in data or 'email' not in data:
        errors.append("Required fields are missing.")
    if errors:
        return {"errors": errors}, 400

    try:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        flash("User updated successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_user_service(id: int):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def change_password_service(id: int, data: dict):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    if 'password' not in data or 'confirm_password' not in data:
        return {"error": "Password and confirm password are required."}, 400

    if data['password'] != data['confirm_password']:
        return {"error": "Passwords do not match."}, 400

    try:
        user.password = data['password']
        db.session.commit()
        return {"message": "Password changed successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_avatar_service(id: int):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    avatar = request.files.get('avatar')
    if not avatar or avatar.filename == '':
        flash("Please select an avatar file.", "error")
        return "", 400
    if not allowed_file(avatar.filename):
        flash(
            "Invalid file format. Only PNG, JPG, JPEG, and GIF files are allowed.", "error")
        return "", 400

    filename = secure_filename(avatar.filename)
    avatar_path = os.path.join('avatars', filename)
    save_path = os.path.join('website', 'static', avatar_path)

    try:
        # Save the avatar image file
        avatar.save(save_path)
        user.avatar = avatar_path.replace(os.sep, '/')
        db.session.commit()
        flash("Avatar uploaded successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
