from flask import jsonify
#from flask_jwt_extended import JWTManager


def register_jwt_handlers(jwt):
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        # Token malformado / assinatura inválida
        return jsonify({
            "type": "/errors/auth/invalid-token",
            "title": "Invalid token",
            "status": 401,
            "detail": error
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        # Token não enviado
        return jsonify({
            "type": "/errors/auth/missing-token",
            "title": "Missing token",
            "status": 401,
            "detail": error
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "type": "/errors/auth/expired-token",
            "title": "Expired token",
            "status": 401,
            "detail": "The token has expired"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "type": "/errors/auth/revoked-token",
            "title": "Revoked token",
            "status": 401,
            "detail": "The token has been revoked"
        }), 401

    @jwt.needs_fresh_token_loader
    def fresh_token_required_callback(jwt_header, jwt_payload):
        return jsonify({
            "type": "/errors/auth/fresh-token-required",
            "title": "Fresh token required",
            "status": 401,
            "detail": "A fresh token is required"
        }), 401
