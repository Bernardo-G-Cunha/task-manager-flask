from flask import Blueprint

from app.routes.tasks import tasks_bp
from app.routes.auth import auth_bp

def register_bp(app):

    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(auth_bp, url_prefix='/auth')
