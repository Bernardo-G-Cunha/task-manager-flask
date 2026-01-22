from flask import request, jsonify
from sqlalchemy.exc import OperationalError, IntegrityError
from marshmallow import ValidationError

from app.exceptions import (
    ProblemDetailException
)

def register_error_handlers(app):
    @app.errorhandler(ProblemDetailException)
    def handle_problem_detail_exception(exc):
        return jsonify({
            "type": exc.type,
            "title": exc.title,
            "status": exc.status,
            "detail": exc.detail,
            "instance": request.path
        
            }), exc.status
    

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc):
        return jsonify({
            "type": "/errors/validation",
            "title": "Validation error",
            "status": 422,
            "detail": exc.messages,
            "instance": request.path
        }), 422

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(exc):
        return jsonify({
            "type": "/errors/database",
            "title": "Database integrity error",
            "status": 500,
            "detail": "A database integrity constraint was violated.",
            "instance": request.path
        }), 500

    @app.errorhandler(OperationalError)
    def handle_operational_error(exc):
        return jsonify({
            "type": "/errors/database",
            "title": "Database operational error",
            "status": 500,
            "detail": "Database service is temporarily unavailable.",
            "instance": request.path
        }), 500

    @app.errorhandler(Exception)
    def handle_generic_error(exc):
        return jsonify({
            "type": "/errors/internal",
            "title": "Internal server error",
            "status": 500,
            "detail": "An unexpected error occurred.",
            "instance": request.path
        }), 500