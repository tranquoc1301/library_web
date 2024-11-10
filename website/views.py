from flask import Blueprint, render_template, request
from .models import Books, Category  # Đảm bảo bạn đã định nghĩa các model này
from .books import controllers as book_controllers
from .category import controllers as category_controllers
from .students import controllers as student_controllers
from .services.authorize import role_required

# Tạo một blueprint cho các route
views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    books = book_controllers.get_all_books_service()
    books = books[:6]
    categories = category_controllers.get_all_categories_service()
    categories = categories[:5]

    categories_with_count = []
    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('index.html', books=books, categories=categories)


@views.route('/books', methods=['GET'])
def books():
    books = book_controllers.get_all_books_service()
    return render_template('book.html', books=books)


@views.route('/books/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    book = book_controllers.get_book_by_id_service(book_id)
    book.category_name = category_controllers.get_category_by_id_service(
        book.category_id).category
    return render_template('book_detail.html', book=book)


@views.route('/books/search', methods=['GET'])
def search_books():
    title = request.args.get('title')
    books = book_controllers.search_books_service(title)
    return render_template("book.html", books=books)


@views.route('/books/category/<int:category_id>', methods=['GET'])
def books_by_category_id(category_id):
    books = book_controllers.get_books_by_category_id_service(category_id)
    return render_template('book.html', books=books)


@views.route('/books/<int:book_id>/read', methods=['GET'])
@role_required(['user', 'admin'])
def read_book(book_id):
    return book_controllers.load_pdf_service(book_id)


@views.route('/books/<int:book_id>/download', methods=['GET'])
@role_required(['user', 'admin'])
def download_book(book_id):
    return book_controllers.download_book_service(book_id)


@views.route('/categories')
def category():
    categories = category_controllers.get_all_categories_service()
    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('category.html', categories=categories)


@views.route('/student/<student_id>/profile', methods=['GET'])
@role_required(['user', 'admin'])
def profile(student_id):
    return render_template('profile.html', user=student_controllers.get_student_by_id_service(student_id))


@views.route('/student/<student_id>/profile/upload-avatar', methods=['POST'])
@role_required('user')
def upload_avatar(student_id):
    return student_controllers.upload_avatar_service(student_id)


@views.route('/student/<student_id>/profile/update', methods=['POST'])
@role_required('user')
def update_profile(student_id):
    return student_controllers.update_student_service(student_id)


@views.app_errorhandler(401)
def forbidden(e):
    return render_template('401.html'), 401
