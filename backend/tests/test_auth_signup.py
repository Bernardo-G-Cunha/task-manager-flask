from app.models import User, Event
from app.extensions import db


def test_signup_success(client, app):
    response = client.post(
        "/auth/signup",
        json={
            "username": "bernardo",
            "email": "bernardo@email.com",
            "password": "Valid_password@1"
        }
    )
    data = response.get_json()

    assert response.status_code == 201
    
    assert data["message"] == "Successfully signed up"

    with app.app_context():
        user = db.session.query(User).all()
        event = db.session.query(Event).first()

        assert user is not None
        assert user[0].username == "bernardo"
        assert event.event_type == "USER_CREATED"


def test_signup_invalid_data(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "email_sem_username@gmail.com"
        }
    )

    assert response.status_code == 422


def test_signup_duplicate_user(client):
    payload = {
        "username": "bernardo",
        "email": "bernardo@email.com",
        "password": "Valid_password@2"
    }

    client.post("/auth/signup", json=payload)
    response = client.post("/auth/signup", json=payload)

    assert response.status_code == 409


def test_signup_invalid_password(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "error_user",
            "email": "error@email.com",
            "password": "weak"
        }
    )

    assert response.status_code == 400
