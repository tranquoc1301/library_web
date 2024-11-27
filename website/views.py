from flask import Blueprint, render_template, session, redirect, url_for, flash, request, g
from .models import Books, Category, Favorites
from .books import controllers as book_controllers
from .category import controllers as category_controllers
from .users import controllers as user_controllers
from .favorites import controllers as favorite_controllers
from .comments import controllers as comment_controllers
from .services.authorize import role_required
from .db import db

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
    current_page = request.args.get('page', 1, type=int)
    books_per_page = 12
    books = book_controllers.get_all_books_service()

    total_books = len(books)
    total_pages = max((total_books + books_per_page - 1) // books_per_page, 1)

    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    start = (current_page - 1) * books_per_page
    end = start + books_per_page
    books = books[start:end]
    return render_template('book.html', books=books, current_page=current_page, total_pages=total_pages)


@views.route('/admin/books', methods=['GET'])
@role_required('admin')
def admin_books():
    current_page = request.args.get('page', 1, type=int)
    books_per_page = 10

    # Fetch all books and categories
    all_books = book_controllers.get_all_books_service()
    categories = category_controllers.get_all_categories_service()

    total_books = len(all_books)
    total_pages = max((total_books + books_per_page - 1) // books_per_page, 1)

    # Prevent invalid page numbers
    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    # Pagination slicing
    start = (current_page - 1) * books_per_page
    end = start + books_per_page
    books = all_books[start:end]

    return render_template('admin/books.html',
                           books=books,
                           categories=categories,
                           current_page=current_page,
                           total_pages=total_pages)
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
    return render_template("book_search.html", books=books)

# Books by category


@views.route('/books/category/<int:category_id>', methods=['GET'])
def books_by_category_id(category_id):
    books = book_controllers.get_books_by_category_id_service(category_id)
    current_page = request.args.get('page', 1, type=int)
    books_per_page = 12

    total_books = len(books)
    total_pages = max((total_books + books_per_page - 1) // books_per_page, 1)

    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    start = (current_page - 1) * books_per_page
    end = start + books_per_page
    books = books[start:end]
    return render_template('book.html', books=books, current_page=current_page, total_pages=total_pages)

# Reading and downloading books (protected routes)


@views.route('/books/<int:book_id>/read', methods=['GET'])
@role_required(['user', 'admin'])
def read_book(book_id):
    book = Books.query.get(book_id)
    if book:
        # Cập nhật số lượt xem
        book.view_count += 1
        db.session.commit()
    return book_controllers.load_pdf_service(book_id)


@views.route('/books/<int:book_id>/download', methods=['GET'])
@role_required(['user', 'admin'])
def download_book(book_id):
    user_id = session.get('user_id')
    user = user_controllers.get_user_by_id_service(user_id)
    if user.is_active == True:
        book = Books.query.get(book_id)
        if book:
            # Cập nhật số lượt download
            book.download_count += 1
            db.session.commit()
        return book_controllers.download_book_service(book_id)
    else:
        flash("Your account is not activated. Please activate your account in Profile to use this feature.", category="warning")
    return redirect(request.referrer)


@views.route('/books/create', methods=['POST'])
@role_required('admin')
def add_book():
    message, status = book_controllers.add_book_service()

    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/books/<int:book_id>/update', methods=['POST'])
@role_required('admin')
def update_book(book_id):
    message, status = book_controllers.update_book_service(book_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/books/<int:book_id>/delete', methods=['POST'])
@role_required('admin')
def delete_book(book_id):
    message, status = book_controllers.delete_book_service(book_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


# Categories listing route


@views.route('/categories')
def category():
    categories = category_controllers.get_all_categories_service()
    for category in categories:
        category.book_count = len(
            book_controllers.get_books_by_category_id_service(category.id))

    return render_template('category.html', categories=categories)


@views.route('/admin/categories', methods=['GET'])
@role_required('admin')
def admin_categories():
    categories = category_controllers.get_all_categories_service()
    return render_template('admin/categories.html', categories=categories)


@views.route('/categories/create', methods=['POST'])
@role_required('admin')
def add_category():
    message, status = category_controllers.add_category_service()
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/categories/<int:category_id>/update', methods=['POST'])
@role_required('admin')
def update_category(category_id):
    message, status = category_controllers.update_category_service(category_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/categories/<int:category_id>/delete', methods=['POST'])
@role_required('admin')
def delete_category(category_id):
    message, status = category_controllers.delete_category_service(category_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)

# User profile route


@views.route('/admin/users', methods=['GET'])
@role_required('admin')
def admin_users():
    current_page = request.args.get('page', 1, type=int)
    users_per_page = 10
    users = user_controllers.get_all_users_service()

    total_users = len(users)
    total_pages = max((total_users + users_per_page - 1) // users_per_page, 1)

    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    start = (current_page - 1) * users_per_page
    end = start + users_per_page
    users = users[start:end]
    return render_template('admin/users.html', users=users, current_page=current_page, total_pages=total_pages)


@views.route('/admin/users/create', methods=['POST'])
@role_required('admin')
def add_user():
    message, status = user_controllers.add_user_service()
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/admin/users/<int:user_id>/update', methods=['POST'])
@role_required('admin')
def update_user(user_id):
    message, status = user_controllers.update_user_service(user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


@views.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    message, status = user_controllers.delete_user_service(user_id)
    flash(message, category='success' if status == 200 else 'error')
    return redirect(request.referrer)


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
@role_required(['user', 'admin'])
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
@role_required(['user', 'admin'])
def delete_comment(book_id, comment_id):
    message, status = comment_controllers.delete_comment_service(comment_id)
    flash(message, category="success" if status == 200 else "error")
    return redirect(request.referrer)


@views.route('/admin/dashboard', methods=['GET'])
@role_required('admin')
def dashboard():
    total_users = len(user_controllers.get_all_users_service())
    total_books = len(book_controllers.get_all_books_service())
    total_categories = len(category_controllers.get_all_categories_service())

    return render_template('admin/dashboard.html', total_users=total_users, total_books=total_books, total_categories=total_categories)


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
