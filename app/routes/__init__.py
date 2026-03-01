from .auth import auth_bp
from .tasks import tasks_bp
from .admin import admin_bp

__all__ = [
    "auth_bp",
    "tasks_bp",
    "admin_bp",
]
