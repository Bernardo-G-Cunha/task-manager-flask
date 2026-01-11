# tests/conftest.py
import pytest
import os
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://taskuser:taskpass@localhost:5432/taskmanager_test",
        "SECRET_KEY": "test",
        "JWT_SECRET_KEY": "test"
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
