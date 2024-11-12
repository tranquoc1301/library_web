from functools import wraps
from flask import abort, session
from ..models import Users


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return abort(401)  # Unauthorized nếu chưa đăng nhập

            user = Users.query.get(user_id)
            if user.role not in roles:
                return abort(403)  # Forbidden nếu vai trò không phù hợp

            return f(*args, **kwargs)
        return decorated_function
    return decorator
