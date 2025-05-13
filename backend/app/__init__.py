from flask import Flask
from app.extensions import db, ma, jwt, migrate, bcrypt
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.config import Config
from app.models import *


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)   
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    
    #Register blueprints

    return app





 


#-------------------------------------------------------------------------------
