from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.auth import ForbiddenError

def admin_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()
            role = claims["role"]

            if role != "ADMIN":
                raise ForbiddenError()

            return fn(*args, **kwargs)

        return wrapper
    return decorator
