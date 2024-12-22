from flask import request, flash
from ..db import db
from ..models import Users
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os
bcrypt = Bcrypt()

ALLOWED_COVER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
AVATAR_UPLOAD_FOLDER = os.path.join("website", "static", "avatars")


def allowed_cover_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_COVER_EXTENSIONS


def add_user_service():
    data = request.form
    avatar = request.files.get('avatar')
    errors = []

    # Kiểm tra các trường bắt buộc
    required_fields = ['fullname', 'username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required.")

    # Kiểm tra định dạng ảnh đại diện
    if avatar and not allowed_cover_file(avatar.filename):
        errors.append(
            "Invalid avatar file format. Allowed formats: png, jpg, jpeg, gif.")

    # Trả về lỗi nếu có
    if errors:
        return {"errors": errors}, 400

    try:
        # Xử lý ảnh đại diện (nếu có)
        avatar_filename = None
        if avatar:
            # Đảm bảo thư mục lưu ảnh tồn tại
            os.makedirs(AVATAR_UPLOAD_FOLDER, exist_ok=True)

            # Lưu ảnh vào thư mục
            avatar_filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(AVATAR_UPLOAD_FOLDER, avatar_filename)
            avatar.save(avatar_path)

        hashed_password = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        # Tạo đối tượng người dùng mới
        new_user = Users(
            fullname=data['fullname'],
            username=data['username'],
            email=data['email'],
            # Cần mã hóa mật khẩu trước khi lưu
            password=hashed_password,
            avatar=f"avatars/{avatar_filename}" if avatar else "avatars/user.png"
        )

        # Thêm vào database
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully", "success")
        return "", 200
    except Exception as e:
        # Rollback nếu xảy ra lỗi
        db.session.rollback()
        flash(f"Failed to add user: {str(e)}", "danger")
        return {"error": "An error occurred while adding the user."}, 500


def get_all_users_service():
    all_users = Users.query.all()
    return all_users


def get_user_by_id_service(id: int):
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    return user


def update_user_service(id: int):
    # Lấy thông tin người dùng từ database
    user = Users.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    data = request.form
    avatar = request.files.get('avatar')

    # Kiểm tra các trường bắt buộc
    if not data.get('fullname') or not data.get('email'):
        flash("All fields are required", "danger")
        return "", 400
    if Users.query.filter_by(email=data['email']).first() and data['email'] != user.email:
        flash("Email already exists", "danger")
        return "", 400

    # Kiểm tra định dạng ảnh đại diện (nếu có)
    if avatar and not allowed_cover_file(avatar.filename):
        flash("Invalid avatar file format - allowed: png, jpg, jpeg, gif", "danger")
        return "", 400

    try:
        # Cập nhật thông tin cơ bản
        user.fullname = data['fullname']
        user.email = data['email']
        is_active = data.get('is_active')  # Lấy giá trị của 'is_active'

        if is_active == '1':
            user.is_active = 1
        else:
            user.is_active = 0
        if avatar:
            # Đảm bảo thư mục lưu ảnh tồn tại
            os.makedirs(AVATAR_UPLOAD_FOLDER, exist_ok=True)

            # Lưu ảnh với tên an toàn
            avatar_filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(AVATAR_UPLOAD_FOLDER, avatar_filename)
            avatar.save(avatar_path)

            # Cập nhật đường dẫn ảnh trong cơ sở dữ liệu
            user.avatar = f"avatars/{avatar_filename}"

        # Cập nhật vai trò (role) nếu có trong request
        if 'role' in data:
            user.role = data['role']

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        flash("User updated successfully", "success")
        return "", 200
    except Exception as e:
        # Rollback nếu có lỗi
        db.session.rollback()
        flash(f"Failed to update user: {str(e)}", "danger")
        return "", 500


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
        flash("Please select an avatar file.", "danger")
        return "", 400
    if not allowed_file(avatar.filename):
        flash(
            "Invalid file format. Only PNG, JPG, JPEG, and GIF files are allowed.", "danger")
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
