from flask import send_file, request, jsonify, abort, flash
from ..db import db
from ..library_ma import BookSchema
from ..models import Books
from sqlalchemy.exc import IntegrityError
import os

book_schema = BookSchema()
books_schema = BookSchema(many=True)


def add_book_service():
    # Lấy dữ liệu từ form
    title = request.form.get('title')
    category_id = request.form.get('category_id')
    publish_year = request.form.get('publish_year')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    summary = request.form.get('summary')
    cover = request.form.get('cover')
    file_path = request.form.get('file_path')

    # Kiểm tra dữ liệu từ form (có thể thêm các điều kiện kiểm tra dữ liệu)
    if not all([title, category_id, publish_year, author, publisher]):
        flash("All fields are required", "error")
        # return redirect(url_for('add_book'))

    try:
        # Tạo mới một cuốn sách từ dữ liệu form
        new_book = Books(
            category_id=category_id,
            title=title,
            publish_year=publish_year,
            author=author,
            publisher=publisher,
            summary=summary,
            cover=cover,
            file_path=file_path
        )

        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully", "success")

    except IntegrityError:
        db.session.rollback()
        flash("Book with this title already exists", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")


def get_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")
    return book  # Trả về đối tượng sách cho template


def get_views_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")
    return book.view_count


def get_downloads_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")
    return book.download_count


def get_all_books_service():
    book_list = Books.query.all()
    return book_list


def get_books_by_category_id_service(category_id):
    book_list = Books.query.filter_by(category_id=category_id).all()
    return book_list


def load_pdf_service(book_id: int):
    book = Books.query.get(book_id)
    if not book:
        abort(404, description="Book not found")

    pdf_path = os.path.normpath(os.path.join('static', book.file_path))

    try:
        return send_file(pdf_path, as_attachment=False)
    except Exception as e:
        return jsonify({"error": "Failed to send the PDF file", "details": str(e)}), 500


def download_book_service(book_id: int):
    book = Books.query.get(book_id)
    if not book:
        abort(404, description="Book not found")

    pdf_path = os.path.normpath(os.path.join('static', book.file_path))

    try:
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Failed to send the PDF file", "details": str(e)}), 500


def search_books_service(title):
    return Books.query.filter(Books.title.ilike(f"%{title}%")).all()


def update_book_service(id: int):
    book = Books.query.get(id)
    if not book:
        flash("Book not found", "error")
        # Chuyển hướng về danh sách sách nếu không tìm thấy sách
        # return redirect(url_for('views.books'))

    # Lấy dữ liệu từ form
    title = request.form.get('title')
    category_id = request.form.get('category_id')
    publish_year = request.form.get('publish_year')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    summary = request.form.get('summary')
    cover = request.form.get('cover')
    file_path = request.form.get('file_path')

    # Kiểm tra dữ liệu từ form (có thể thêm các điều kiện kiểm tra dữ liệu)
    if not all([title, category_id, publish_year, author, publisher]):
        flash("All fields are required", "error")
        # return redirect(url_for('update_book', id=id))  # Chuyển hướng lại trang sửa nếu thiếu trường dữ liệu

    try:
        # Cập nhật thông tin sách
        book.title = title
        book.category_id = category_id
        book.publish_year = publish_year
        book.author = author
        book.publisher = publisher
        book.summary = summary
        book.cover = cover
        book.file_path = file_path

        db.session.commit()

        flash("Book updated successfully", "success")
        # return redirect(url_for('view_books'))  # Chuyển hướng về danh sách sách sau khi sửa thành công

    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")
        # return redirect(url_for('update_book', id=id))  # Chuyển hướng lại trang sửa nếu có lỗi


def delete_book_service(id: int):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
