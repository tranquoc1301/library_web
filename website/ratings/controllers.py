from ..models import Rating, Books, flash, redirect, url_for
from flask import request, jsonify, abort
from ..db import db
from ..library_ma import RatingSchema
from sqlalchemy.exc import IntegrityError

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)


def add_rating_service():
    # Lấy dữ liệu từ form
    rating_value = request.form.get('rating', type=int)
    book_id = request.form.get('book_id', type=int)
    user_id = request.form.get('user_id', type=int)
    comment = request.form.get('comment')

    # Kiểm tra tính hợp lệ của rating
    if rating_value is None or rating_value < 1 or rating_value > 5:
        flash("Rating must be between 1 and 5.", "error")
        # return redirect(url_for('view_book', book_id=book_id))  # Quay lại trang sách

    if not book_id or not user_id:
        flash("Both book and user are required", "error")
        # return redirect(url_for('view_book', book_id=book_id))  # Quay lại trang sách

    try:
        # Kiểm tra nếu người dùng đã đánh giá cuốn sách này chưa
        existing_rating = Rating.query.filter_by(
            book_id=book_id, user_id=user_id).first()
        if existing_rating:
            flash("You have already rated this book.", "info")
            # return redirect(url_for('view_book', book_id=book_id))  # Quay lại trang sách

        # Tạo đối tượng đánh giá mới
        new_rating = Rating(
            book_id=book_id,
            user_id=user_id,
            rating=rating_value,
            comment=comment
        )

        db.session.add(new_rating)
        db.session.commit()

        average_rating = Rating.query.filter_by(
            book_id=book_id).with_entities(db.func.avg(Rating.rating)).scalar()

        book = Books.query.get(book_id)
        if book:
            book.average_rating = average_rating
            db.session.commit()

        flash("Thank you for your rating!", "success")
        # return redirect(url_for('view_book', book_id=book_id))  # Quay lại trang sách

    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")
        # return redirect(url_for('view_book', book_id=book_id))  # Quay lại trang sách


def get_all_ratings_service(book_id: int):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    return ratings  # Trả về danh sách đánh giá cho template


def update_rating_service(book_id: int, user_id: int):
    rating = Rating.query.filter_by(book_id=book_id, user_id=user_id).first()
    if not rating:
        flash("Rating not found", "error")
        # return redirect(url_for('view_book', book_id=book_id))

    # Lấy dữ liệu từ form
    rating_value = request.form.get('rating', type=int)
    comment = request.form.get('comment')

    # Kiểm tra tính hợp lệ của rating
    if rating_value is not None and (rating_value < 1 or rating_value > 5):
        flash("Rating must be between 1 and 5.", "error")
        # return redirect(url_for('view_book', book_id=book_id))

    try:
        # Cập nhật rating nếu có thay đổi
        if rating_value:
            rating.rating = rating_value
        if comment:
            rating.comment = comment

        db.session.commit()

        # Tính toán lại điểm đánh giá trung bình của sách
        average_rating = Rating.query.filter_by(
            book_id=book_id).with_entities(db.func.avg(Rating.rating)).scalar()

        book = Books.query.get(book_id)
        if book:
            book.average_rating = average_rating
            db.session.commit()

        flash("Your rating has been updated!", "success")
        # Quay lại trang sách
        # return redirect(url_for('view_book', book_id=book_id))

    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")
        # Quay lại trang sách
        # return redirect(url_for('view_book', book_id=book_id))


def delete_rating_service(book_id: int, user_id: int):
    rating = Rating.query.filter_by(
        book_id=book_id, user_id=user_id).first()
    if not rating:
        abort(404, description="Rating not found")

    try:
        db.session.delete(rating)
        db.session.commit()
        return jsonify({"message": "Rating deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
