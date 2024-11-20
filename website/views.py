from flask import Blueprint, render_template, session, redirect, url_for, flash, request, g
from .models import Books, Category, Favorites
from .books import controllers as book_controllers
from .category import controllers as category_controllers
from .users import controllers as user_controllers
from .favorites import controllers as favorite_controllers
from .comments import controllers as comment_controllers
from .services.authorize import role_required

# Create a blueprint for the routes
views = Blueprint('views', __name__)

# Index route


@views.route('/', methods=['GET'])
def index():
    user = user_controllers.get_user_by_id_service(session.get('user_id'))
    books = book_controllers.get_all_books_service()[:6]
    categories = category_controllers.get_all_categories_service()[:5]

    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('index.html', books=books, categories=categories, user=user)

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
    comments = comment_controllers.get_comments_by_book_id_service(book_id)
    users = {comment.user_id: user_controllers.get_user_by_id_service(
        comment.user_id) for comment in comments}
    
    return render_template('book_detail.html', book=book, comments=comments, users=users)

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
@role_required(['user', 'admin'])
def upload_avatar():
    user_id = session.get('user_id')
    message, status = user_controllers.upload_avatar_service(user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)
# Update profile route


@views.route('/user/profile/update', methods=['POST'])
@role_required(['user', 'admin'])
def update_profile():
    user_id = session.get('user_id')
    message, status = user_controllers.update_user_service(user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)

# Favorite books route


@views.route('/user/favorites', methods=['GET'])
@role_required('user')
def favorites():
    user_id = session.get('user_id')
    favorites_books = favorite_controllers.get_favorites_books_by_user_id_service(
        user_id)
    return render_template('user/favorites.html', books=favorites_books)

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


@views.route('/book/<book_id>/comments', methods=['POST'])
@role_required('user')
def add_comment(book_id):
    user_id = session.get('user_id')
    content = request.form.get('content')
    message, status = comment_controllers.add_comment_service(
        book_id, user_id, content)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/books/<int:book_id>/comments/<int:comment_id>/edit', methods=['POST'])
@role_required('user')
def edit_comment(book_id, comment_id):
    content = request.form.get('content')
    message, status = comment_controllers.update_comment_service(
        comment_id, content)
    flash(message, category="success" if status == 200 else "error")
    return redirect(url_for('views.book_detail', book_id=book_id))


@views.route('/books/<int:book_id>/comments/<int:comment_id>/delete', methods=['POST'])
@role_required('user')
def delete_comment(book_id, comment_id):
    message, status = comment_controllers.delete_comment_service(comment_id)
    flash(message, category="success" if status == 200 else "error")
    return redirect(request.referrer)


@views.app_errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@views.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@views.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = user_controllers.get_user_by_id_service(user_id)
    else:
        g.user = None
