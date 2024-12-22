from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from ..db import db
from ..models import Category
from sqlalchemy.exc import IntegrityError
import os

# Định dạng file ảnh cho phép
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'website/static/category'  # Thư mục lưu trữ ảnh


def allowed_cover_file(filename):
    """Kiểm tra định dạng file ảnh có hợp lệ không"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def add_category_service():
    """Thêm một danh mục mới"""
    category_name = request.form.get('category')
    image = request.files.get('image')  # Đảm bảo lấy file ảnh từ form

    if not category_name:
        flash("Category name is required", "danger")
        return redirect(url_for('views.admin_categories'))  # Redirect directly

    if image and not allowed_cover_file(image.filename):
        flash("Invalid image format. Allowed formats: png, jpg, jpeg, gif.", "danger")
        return "", 400  # Return directly on error
    try:
        # Kiểm tra nếu danh mục đã tồn tại
        existing_category = Category.query.filter_by(
            category=category_name).first()
        if existing_category:
            flash("Category already exists", "danger")
            # Redirect directly
            return "", 400
        # Lưu ảnh vào thư mục
        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)

        # Tạo và lưu danh mục mới
        new_category = Category(
            category=category_name,
            image=f"category/{image_filename}" if image_filename else None
        )
        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully", "success")
        # Redirect after success
        return "", 201
    except IntegrityError:
        db.session.rollback()
        flash("Category with this name already exists.", "danger")
        return "", 400
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        # Redirect on general error
        return "", 500


def get_all_categories_service():
    """Lấy tất cả danh mục"""
    return Category.query.all()


def get_category_by_id_service(category_id: int):
    """Lấy danh mục theo ID"""
    category = Category.query.get(category_id)
    if not category:
        flash("Category not found", "danger")
    return category


def update_category_service(category_id: int):
    """Cập nhật thông tin danh mục"""
    category = Category.query.get(category_id)
    if not category:
        flash("Category not found", "danger")
        return "", 404

    category_name = request.form.get('category')
    image = request.files.get('image')

    if not category_name:
        flash("Category name is required", "danger")
        return "", 400

    try:
        # Cập nhật thông tin danh mục
        category.category = category_name

        if image:
            if not allowed_cover_file(image.filename):
                flash(
                    "Invalid image format. Allowed formats: png, jpg, jpeg, gif.", "danger")
                return redirect(url_for('views.admin_categories'))

            image_filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)
            # Lưu đường dẫn đúng vào DB
            category.image = f"category/{image_filename}"

        db.session.commit()

        flash("Category updated successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return "", 500


def delete_category_service(category_id: int):
    """Xóa danh mục"""
    category = Category.query.get(category_id)
    if not category:
        flash("Category not found", "danger")
        return "", 404
    try:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return "", 500
