from app.models.user import User
from app.extensions import db


def test_signup_success(client, app):
    response = client.post(
        "/auth/signup",
        json={
            "username": "bernardo",
            "email": "bernardo@email.com",
            "password": "test_8_digits"
        }
    )
    data = response.get_json()

    assert response.status_code == 201
    
    assert data["message"] == "Successfully signed up"

    with app.app_context():
        user = db.session.query(User).all()
        
        assert user is not None
        assert user[0].username == "bernardo"


def test_signup_invalid_data(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "email-sem-username"
            # Missing needed fields
        }
    )

    assert response.status_code == 422


def test_signup_duplicate_user(client):
    payload = {
        "username": "bernardo",
        "email": "bernardo@email.com",
        "password": "123456rervef"
    }

    client.post("/auth/signup", json=payload)
    response = client.post("/auth/signup", json=payload)

    assert response.status_code == 409
