from flask import Blueprint, render_template, request
from .models import Books, Category  # Đảm bảo bạn đã định nghĩa các model này
from .books import controllers as book_controllers
from .category import controllers as category_controllers

# Tạo một blueprint cho các route
views = Blueprint('views', __name__)


@views.route('/')
def index():
    books = book_controllers.get_all_books_service()
    books = books[:6]
    categories = category_controllers.get_all_categories_service()
    categories = categories[:5]
    return render_template('index.html', books=books, categories=categories)


@views.route('/books')
def books():
    books = book_controllers.get_all_books_service()
    return render_template('book.html', books=books)


@views.route('/categories')
def category():
    categories = category_controllers.get_all_categories_service()
    return render_template('category.html', categories=categories)
