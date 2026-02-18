import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.extensions import db, ma, jwt, migrate, bcrypt
from app.routes import auth_bp, tasks_bp, admin_bp
from app.exceptions import register_error_handlers
from app.auth import register_jwt_handlers
from app.extensions import limiter


def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/')
    
    # Default configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Environment configuration
    if test_config:
        app.config.update(test_config)
        app.config["RATELIMIT_ENABLED"] = False
    else:
        # Dev/production
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
        
        if os.environ.get("FLASK_ENV") == "production":
            app.config["RATELIMIT_STORAGE_URI"] = os.environ.get(
                "REDIS_URL",
                "redis://localhost:6379/0"
            )

    app.url_map.strict_slashes = False

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "swagger_ui": True,
        "specs_route": "/docs/",
    }

    template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "Production-ready REST API",
        "version": "1.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <JWT>"
        }
    }
}


    swagger = Swagger(app, config=swagger_config, template=template)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    limiter.init_app(app)

    CORS(app, origins=["http://127.0.0.1:5500"], supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/v1/tasks')
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")
    
    register_jwt_handlers(jwt)
    register_error_handlers(app)

    return app
