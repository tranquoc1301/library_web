from flask import request, jsonify, abort, flash
from ..db import db
from ..library_ma import FavoriteSchema
from ..models import Favorites, Books
from sqlalchemy.exc import IntegrityError

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)


def add_favorite_service(book_id, user_id):
    if not book_id or not user_id:
        return "Both book and user are required", 400

    try:
        # Kiểm tra nếu đã tồn tại trong cơ sở dữ liệu
        existing_favorite = Favorites.query.filter_by(
            book_id=book_id, user_id=user_id).first()
        if existing_favorite:
            flash("Book already added to favorites", "warning")
            return "", 200

        new_favorite = Favorites(book_id=book_id, user_id=user_id)
        db.session.add(new_favorite)
        db.session.commit()

        flash("Book added to favorites successfully", "success")
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash("Failed to add book to favorites", "error")
        return f"An unexpected error occurred: {str(e)}", 500


def get_favorites_books_by_user_id_service(user_id: int):
    favorites_list = Favorites.query.filter_by(user_id=user_id).all()

    if not favorites_list:
        abort(404, description="No favorite book found for this user")

    favorite_book_ids = [favorite.book_id for favorite in favorites_list]

    favorites_books = Books.query.filter(Books.id.in_(favorite_book_ids)).all()

    return favorites_books


def get_favorite_by_user_id_service(user_id: int):
    favorites_list = Favorites.query.filter_by(user_id=user_id).all()
    if not favorites_list:
        abort(404, description="No favorite book found for this user")
    return favorites_list


def delete_favorite_book_service(book_id: int, user_id: int):
    favorite = Favorites.query.filter_by(
        book_id=book_id, user_id=user_id).first()
    if not favorite:
        abort(404, description="Favorite not found")

    try:
        db.session.delete(favorite)
        db.session.commit()
        flash("Favorite book deleted successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash("Failed to delete favorite book", "error")
        return f"An unexpected error occurred: {str(e)}", 500
