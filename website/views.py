from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .models import Books, Category, Favorites
from .books import controllers as book_controllers
from .category import controllers as category_controllers
from .users import controllers as user_controllers
from .favorites import controllers as favorite_controllers
from .services.authorize import role_required

# Create a blueprint for the routes
views = Blueprint('views', __name__)

# Index route


@views.route('/', methods=['GET'])
def index():
    books = book_controllers.get_all_books_service()[:6]
    categories = category_controllers.get_all_categories_service()[:5]

    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('index.html', books=books, categories=categories)

# Books listing route


@views.route('/books', methods=['GET'])
def books():
    books = book_controllers.get_all_books_service()
    return render_template('book.html', books=books)

# Book details route


@views.route('/books/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    book = book_controllers.get_book_by_id_service(book_id)
    book.category_name = category_controllers.get_category_by_id_service(
        book.category_id).category
    return render_template('book_detail.html', book=book)

# Search books by title


@views.route('/books/search', methods=['GET'])
def search_books():
    title = request.args.get('title')
    books = book_controllers.search_books_service(title)
    return render_template("book.html", books=books)

# Books by category


@views.route('/books/category/<int:category_id>', methods=['GET'])
def books_by_category_id(category_id):
    books = book_controllers.get_books_by_category_id_service(category_id)
    return render_template('book.html', books=books)

# Reading and downloading books (protected routes)


@views.route('/books/<int:book_id>/read', methods=['GET'])
@role_required(['user', 'admin'])
def read_book(book_id):
    return book_controllers.load_pdf_service(book_id)


@views.route('/books/<int:book_id>/download', methods=['GET'])
@role_required(['user', 'admin'])
def download_book(book_id):
    user_id = session.get('user_id')
    user = user_controllers.get_user_by_id_service(user_id)
    if user.is_active == True:
        return book_controllers.download_book_service(book_id)
    else:
        flash("Your account is not activated. Please activate your account in Profile to use this feature.", category="warning")
    return redirect(request.referrer)

# Categories listing route


@views.route('/categories')
def category():
    categories = category_controllers.get_all_categories_service()
    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('category.html', categories=categories)

# User profile route


@views.route('/user/profile', methods=['GET'])
@role_required(['user', 'admin'])
def profile():
    user_id = session.get('user_id')
    return render_template('profile.html', user=user_controllers.get_user_by_id_service(user_id))

# Avatar upload route


@views.route('/user/profile/upload-avatar', methods=['POST'])
@role_required('user')
def upload_avatar():
    user_id = session.get('user_id')
    return user_controllers.upload_avatar_service(user_id)

# Update profile route


@views.route('/user/profile/update', methods=['POST'])
@role_required('user')
def update_profile():
    user_id = session.get('user_id')
    return user_controllers.update_user_service(user_id)

# Favorite books route


@views.route('/user/favorites', methods=['GET'])
@role_required('user')
def favorites():
    user_id = session.get('user_id')
    favorites_books = favorite_controllers.get_favorites_books_by_user_id_service(
        user_id)
    return render_template('favorites.html', books=favorites_books)

# Add to favorites route


@views.route('/user/favorites/<int:book_id>', methods=['POST'])
@role_required('user')
def add_to_favorites(book_id):
    user_id = session.get('user_id')
    message, status = favorite_controllers.add_favorite_service(
        book_id, user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)

# Remove from favorites route


@views.route('/user/favorites/remove/<int:book_id>', methods=['POST'])
@role_required('user')
def remove_from_favorites(book_id):
    user_id = session.get('user_id')
    message, status = favorite_controllers.delete_favorite_book_service(
        book_id, user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)

# Error handler


@views.app_errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@views.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
