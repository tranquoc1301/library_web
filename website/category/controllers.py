from flask import request, jsonify, abort
from ..db import db
from ..library_ma import CategorySchema
from ..models import Category
from sqlalchemy.exc import IntegrityError

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


from flask import render_template, request, redirect, url_for, flash
from ..db import db
from ..models import Category


def add_category_service():
    # Lấy dữ liệu từ form
    category_name = request.form.get('category')
    image = request.form.get('image')

    # Kiểm tra nếu thiếu trường bắt buộc
    if not category_name:
        flash("Category name is required", "error")
        # return redirect(url_for('add_category'))  # Quay lại trang thêm danh mục

    try:
        # Kiểm tra nếu danh mục đã tồn tại
        existing_category = Category.query.filter_by(category=category_name).first()
        if existing_category:
            flash("Category already exists", "error")
            # return redirect(url_for('add_category'))  # Quay lại trang thêm danh mục

        # Tạo mới danh mục
        new_category = Category(
            category=category_name,
            image=image
        )

        db.session.add(new_category)
        db.session.commit()

        flash("Category added successfully", "success")
        # return redirect(url_for('views.categories'))  # Quay về trang danh sách danh mục

    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")
        # return redirect(url_for('add_category'))  # Quay lại trang thêm danh mục nếu có lỗi



def get_all_categories_service():
    categories = Category.query.all()
    return categories  # Trả về danh sách danh mục cho template


def get_category_by_id_service(category_id: int):
    category = Category.query.get(category_id)
    if not category:
        abort(404, description="Category not found")
    return category  # Trả về đối tượng danh mục cho template


def update_category_service(category_id: int):
    category = Category.query.get(category_id)
    if not category:
        flash("Category not found", "error")
        # return redirect(url_for('view_categories'))  # Quay lại trang danh sách danh mục

    # Lấy dữ liệu từ form
    category_name = request.form.get('category')
    image = request.form.get('image')

    # Kiểm tra nếu thiếu trường bắt buộc
    if not category_name:
        flash("Category name is required", "error")
        # return redirect(url_for('edit_category', category_id=category_id))  # Quay lại trang chỉnh sửa

    try:
        # Cập nhật thông tin danh mục
        category.category = category_name
        category.image = image

        db.session.commit()

        flash("Category updated successfully", "success")
        # return redirect(url_for('view_categories'))  # Quay lại trang danh sách danh mục

    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")
        # return redirect(url_for('edit_category', category_id=category_id))  # Quay lại trang chỉnh sửa nếu có lỗi


def delete_category_service(category_id: int):
    category = Category.query.get(category_id)
    if not category:
        abort(404, description="Category not found")

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
