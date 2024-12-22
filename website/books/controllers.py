from flask import request, flash
from flask import send_file, request, jsonify, abort, flash
from ..db import db
from werkzeug.utils import secure_filename
from ..library_ma import BookSchema
from ..models import Books
from sqlalchemy.exc import IntegrityError
import os

ALLOWED_COVER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}

# Hàm kiểm tra tệp ảnh bìa hợp lệ


def allowed_cover_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_COVER_EXTENSIONS

# Hàm kiểm tra tệp PDF hợp lệ


def allowed_pdf_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PDF_EXTENSIONS


def add_book_service():
    # Lấy dữ liệu từ form
    title = request.form.get('title')
    category_id = request.form.get('category')
    publish_year = request.form.get('publish_year')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    summary = request.form.get('summary')
    cover = request.files.get('cover')
    pdf = request.files.get('pdf')
    cover_path = None
    pdf_path = None

    # Kiểm tra dữ liệu bắt buộc
    if not all([title, category_id, publish_year, author, publisher]):
        flash("All fields are required", "danger")
        return "", 400

    # Đảm bảo thư mục tồn tại
    cover_dir = os.path.join('website', 'static', 'books', 'covers')
    pdf_dir = os.path.join('website', 'static', 'books', 'pdfs')

    if not os.path.exists(cover_dir):
        os.makedirs(cover_dir)
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Xử lý file cover nếu có
    if cover and allowed_cover_file(cover.filename):
        try:
            cover_filename = secure_filename(
                cover.filename)  # Làm sạch tên file
            cover_path = os.path.join(cover_dir, cover_filename)
            cover.save(cover_path)
            # Lưu đường dẫn trong cơ sở dữ liệu
            cover_path = os.path.join(
                'books', 'covers', cover_filename).replace(os.sep, '/')
        except Exception as e:
            flash(f"Failed to upload cover image: {str(e)}", "danger")
            return "", 500

    # Xử lý file PDF nếu có
    if pdf and allowed_pdf_file(pdf.filename):
        try:
            pdf_filename = secure_filename(pdf.filename)  # Làm sạch tên file
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            pdf.save(pdf_path)
            # Lưu đường dẫn trong cơ sở dữ liệu
            pdf_path = os.path.join(
                'books', 'pdfs', pdf_filename).replace(os.sep, '/')
        except Exception as e:
            flash(f"Failed to upload PDF file: {str(e)}", "danger")
            return "", 500

    try:
        # Lưu sách vào cơ sở dữ liệu
        new_book = Books(
            category_id=category_id,
            title=title,
            publish_year=publish_year,
            author=author,
            publisher=publisher,
            summary=summary,
            cover=cover_path,
            file_path=pdf_path
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully", "success")
        return "", 201
    except IntegrityError:
        db.session.rollback()
        flash("Book with this title already exists", "danger")
        return "", 400
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return "", 500


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
        flash("Book not found", "danger")
        return "", 404

    # Lấy dữ liệu từ form
    title = request.form.get('title')
    category_id = request.form.get('category')
    publish_year = request.form.get('publish_year')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    summary = request.form.get('summary')
    cover = request.files.get('cover')
    pdf = request.files.get('pdf')

    # Kiểm tra dữ liệu bắt buộc
    if not all([title, category_id, publish_year, author, publisher]):
        flash("All fields are required", "danger")
        return "", 400

    # Cập nhật thông tin cơ bản
    book.title = title
    book.category_id = category_id
    book.publish_year = publish_year
    book.author = author
    book.publisher = publisher
    book.summary = summary

    # Xử lý file cover nếu có
    if cover and allowed_cover_file(cover.filename):
        try:
            cover_dir = os.path.join('website', 'static', 'books', 'covers')
            os.makedirs(cover_dir, exist_ok=True)

            cover_filename = secure_filename(cover.filename)
            cover_path = os.path.join(cover_dir, cover_filename)
            cover.save(cover_path)

            # Lưu đường dẫn mới trong DB
            book.cover = os.path.join(
                'books', 'covers', cover_filename).replace(os.sep, '/')
        except Exception as e:
            flash(f"Failed to upload cover image: {str(e)}", "danger")
            return "", 500

    # Xử lý file PDF nếu có
    if pdf and allowed_pdf_file(pdf.filename):
        try:
            pdf_dir = os.path.join('website', 'static', 'books', 'pdfs')
            os.makedirs(pdf_dir, exist_ok=True)

            pdf_filename = secure_filename(pdf.filename)
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            pdf.save(pdf_path)

            # Lưu đường dẫn mới trong DB
            book.file_path = os.path.join(
                'books', 'pdfs', pdf_filename).replace(os.sep, '/')
        except Exception as e:
            flash(f"Failed to upload PDF file: {str(e)}", "danger")
            return "", 500

    try:
        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        flash("Book updated successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return "", 500


def delete_book_service(id: int):
    book = Books.query.get(id)
    if not book:
        abort(404, description="Book not found")

    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully", "success")
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash("Failed to delete book", "danger")
        return "", 500
