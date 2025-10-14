import os
from datetime import timedelta

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY', 'dev-secret')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)