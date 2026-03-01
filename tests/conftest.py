import pytest
import os
from datetime import datetime, timezone
from app import create_app
from app.extensions import db
from app.models import User, Task, Tag, Event
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token
from random import randint

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
        return create_access_token(identity=str(user), additional_claims={"role": "USER"})

@pytest.fixture
def admin_token(app, user):
    with app.app_context():
        return create_access_token(identity=str(user), additional_claims={"role": "ADMIN"})

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

        task = Task(
                user_id=user,
                name=f"Task initial",
                description=f"Task number 0",
                tags=[Tag(name=f"Tag0")],
                done=False,
                creation_date=f"2020-01-02"
            )
        tasks.append(task)

        task = Task(
                user_id=user,
                name=f"Task final",
                description=f"Task number 70",
                tags=[Tag(name=f"Tag70")],
                done=False,
                creation_date=f"2070-01-01"
            )

        tasks.append(task)

        for i in range(1, 29):
            task = Task(
                user_id=user,
                name=f"Task {i}",
                description=f"Task number {i}",
                tags=[Tag(name=f"Tag{i}"), Tag(name=f"Tag{-i}")],
                done=True if i%2 == 0 else False,
                creation_date=f"20{randint(1, 99):02d}-{randint(1,12):02d}-{randint(1,28):02d}"
            )
            tasks.append(task)

        db.session.add_all(tasks)
        db.session.commit()

        return [task.id for task in tasks]

@pytest.fixture
def many_users(app):
    with app.app_context():

        users = []

        for i in range(1, 31):
            user = User(
                username=f"User{randint(1, 100):03d}",
                email=f"email{i}@example.com",
                password = bcrypt.generate_password_hash("123456789").decode("utf-8")
            )
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        return [user.id for user in users]

@pytest.fixture
def many_events(many_users, many_tasks):
    events = []

    event = Event(
            entity_type="task",
            entity_id=many_tasks[19 % len(many_tasks)],
            event_type="TASK_UPDATED",
            actor_user_id=many_users[0],
            old_value={"done": False},
            new_value={"done": True},
            created_at=f"2020-01-02",
        )
    events.append(event)

    event = Event(
            entity_type="user",
            entity_id=many_users[0],
            event_type="USER_CREATED",
            actor_user_id=many_users[0],
            old_value={"done": False},
            new_value={"done": True},
            created_at=f"2070-01-01",
        )

    events.append(event)

    for i in range(18):
        event = Event(
            entity_type="task",
            entity_id=many_tasks[i % len(many_tasks)],
            event_type="TASK_UPDATED",
            actor_user_id=many_users[0],
            old_value={"done": False},
            new_value={"done": True},
            created_at=f"20{randint(1, 99):02d}-{randint(1,12):02d}-{randint(1,28):02d}",
        )
        events.append(event)
    
    db.session.add_all(events)
    db.session.commit()
    return [event.id for event in events]