from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, jwt, migrate
from app.routes.auth import auth
from app.routes.tasks import tasks


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    #Register blueprints

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app)

    return app





 


#-------------------------------------------------------------------------------
