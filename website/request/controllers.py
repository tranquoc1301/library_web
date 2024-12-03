from flask import request, abort, flash
from ..models import Request
from ..db import db
import logging

# Logging setup (nếu cần)
logging.basicConfig(level=logging.INFO)


def get_all_requests_service():
    try:
        requests = Request.query.all()
        return requests
    except Exception as e:
        logging.error(f"Error fetching all requests: {e}")
        abort(500, description="Server error while fetching requests")


def get_request_by_id_service(id):
    try:
        request = Request.query.get(id)
        if not request:
            abort(404, description="Request not found")
        return request
    except Exception as e:
        logging.error(f"Error fetching request by ID {id}: {e}")
        abort(500, description="Server error while fetching request")


def get_requests_by_user_id_service(user_id):
    try:
        requests = Request.query.filter_by(user_id=user_id).all()
        return requests
    except Exception as e:
        logging.error(f"Error fetching requests for user ID {user_id}: {e}")
        abort(500, description="Server error while fetching user requests")


def add_request_service(user_id):
    book_title = request.form.get('book_title')
    book_description = request.form.get('book_description')

    # Kiểm tra dữ liệu đầu vào
    if not user_id or not book_title or not book_description:
        flash("All fields are required", "error")
        return "", 400

    try:
        # Tạo request mới
        new_request = Request(
            user_id=user_id,
            book_title=book_title,
            book_description=book_description
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Book request added successfully", "success")
        return "", 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding request: {e}")
        flash("Failed to add request", "error")
        return "", 500


def update_request_service(request_id, user_id):
    # Lấy dữ liệu từ form
    book_title = request.form.get('book_title')
    book_description = request.form.get('book_description')

    # Kiểm tra dữ liệu đầu vào
    if not book_title or not book_description:
        logging.warning("Missing required fields for updating request")
        return "All fields are required", 400

    try:
        # Tìm request cần cập nhật
        existing_request = Request.query.filter_by(
            id=request_id, user_id=user_id).first()
        if not existing_request:
            logging.warning(
                f"Request ID {request_id} not found or access denied")
            return "Request not found or unauthorized", 404

        # Cập nhật dữ liệu
        existing_request.book_title = book_title
        existing_request.book_description = book_description
        db.session.commit()

        logging.info(f"Request ID {request_id} updated successfully")
        return "Request updated successfully", 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating request with ID {request_id}: {e}")
        return "Failed to update request", 500


def delete_request_service(id):
    try:
        # Tìm request cần xóa
        existing_request = Request.query.get(id)
        if not existing_request:
            abort(404, description="Request not found")

        db.session.delete(existing_request)
        db.session.commit()
        flash("Request deleted successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting request with ID {id}: {e}")
        flash("Failed to delete request", "error")
        return "", 500


def approve_request_service(request_id):
    try:
        existing_request = Request.query.get(request_id)
        if not existing_request:
            abort(404, description="Request not found")

        existing_request.is_approved = True
        db.session.commit()
        flash("Request approved successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error approving request with ID {request_id}: {e}")
        flash("Failed to approve request", "error")
        return "", 500


def reject_request_service(request_id):
    try:
        existing_request = Request.query.get(request_id)
        if not existing_request:
            abort(404, description="Request not found")

        existing_request.is_approved = False
        db.session.commit()
        flash("Request rejected successfully", "success")
        return "", 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error rejecting request with ID {request_id}: {e}")
        flash("Failed to reject request", "error")
        return "", 500
