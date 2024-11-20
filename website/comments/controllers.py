from flask import request, jsonify, abort, flash
from ..db import db
from ..library_ma import CommentSchema
from ..models import Comments


def add_comment_service(book_id, user_id, content):
    try:
        new_comment = Comments(
            book_id=book_id,
            user_id=user_id,
            content=content.strip(),
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully", "success")
        return "", 201
    except Exception as e:
        db.session.rollback()
        flash("Failed to add comment", "error")
        return "", 500


def get_all_comments_service():
    comments = Comments.query.all()
    return comments  # Trả về danh sách bình luận cho template


def get_comment_service(id):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")
    return comment  # Trả về đối tượng bình luận cho template


def get_comments_by_book_id_service(book_id):
    comments = Comments.query.filter_by(book_id=book_id).all()
    return comments


def get_comments_by_user_id_service(user_id):
    comments = Comments.query.filter_by(user_id=user_id).all()
    return comments


def update_comment_service(id, content):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")

    try:
        comment.content = content.strip()
        db.session.commit()
        flash("Comment updated successfully", "success")
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash("Failed to update comment", "error")
        return "", 500


def delete_comment_service(id):
    comment = Comments.query.get(id)
    if not comment:
        abort(404, description="Comment not found")

    try:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully", "success")
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash("Failed to delete comment", "error")
        return "", 500
