from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def rate_limit_key():
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()

        if identity:
            return f"user:{identity}"

    except Exception:
        pass

    return get_remote_address()


db = SQLAlchemy()
ma = Marshmallow()  
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()
limiter = Limiter(
    key_func=rate_limit_key,
    default_limits=[]
)