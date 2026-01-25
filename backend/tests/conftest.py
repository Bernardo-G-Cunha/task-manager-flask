# tests/conftest.py
import pytest
import os
from app import create_app
from app.extensions import db
from app.models import User, Task, Tag
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token

@pytest.fixture(scope="function")
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

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(
            username="test_user",
            email="test@example.com",
            password = bcrypt.generate_password_hash("123456789").decode("utf-8")
        )
        
        db.session.add(user)
        db.session.commit()

        return user.id


@pytest.fixture
def auth_token(app, user):
    with app.app_context():
        return create_access_token(identity=str(user))


@pytest.fixture
def tasks(app, user):
    with app.app_context():
        t1 = Task(user_id=user, name="Test task 1", description="First test task.", due_date="12/02/2027", done=False)
        t2 = Task(user_id=user, name="Test task 2", description="Second test task.", due_date="09/03/2025", done=False, tags=[Tag(name="tag1"), Tag(name="tag2")])
        
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()

        return [t1.id, t2.id]

@pytest.fixture
def many_tasks(app, user):
    with app.app_context():

        tasks = []

        for i in range(1, 31):  # 30 tasks
            task = Task(
                user_id=user,
                name=f"Task {i}",
                description=f"Task number {i}",
                done=False
            )
            tasks.append(task)

        db.session.add_all(tasks)
        db.session.commit()

        return [task.id for task in tasks]