def test_signup_success(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "bernardo",
            "email": "bernardo@email.com",
            "password": "test_8_digits"
        }
    )
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    
    assert data["message"] == "Successfully signed up"


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
