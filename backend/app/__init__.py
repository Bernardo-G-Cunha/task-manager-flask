from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma, jwt, migrate, bcrypt
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.config import Config
from app.models import *
from app.exceptions.error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
      
    app.config.from_object(Config)
    app.url_map.strict_slashes = False
    
    db.init_app(app)
    ma.init_app(app)   
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    CORS(app, origins=["http://127.0.0.1:5500"], supports_credentials=True)

    #Register blueprints

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    register_error_handlers(app)

    return app





 


#-------------------------------------------------------------------------------
