from functools import wraps
from flask import abort, session
from ..models import Students


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            student_id = session.get('student_id')
            if not student_id:
                return abort(401)  # Unauthorized nếu chưa đăng nhập

            student = Students.query.get(student_id)
            if student.role not in roles:
                return abort(403)  # Forbidden nếu vai trò không phù hợp

            return f(*args, **kwargs)
        return decorated_function
    return decorator
