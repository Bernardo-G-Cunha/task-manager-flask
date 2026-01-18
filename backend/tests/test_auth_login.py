def test_login_success(client, user):
    response = client.post(
        "/auth/",
        json={
            "email": "test@example.com",
            "password": "123456789"
        }
    )
    data = response.get_json()

    assert response.status_code == 200

    assert "access_token" in data["data"]


def test_login_authentication_error(client, user):
    response = client.post(
        "/auth/",
        json={
            "email": "false@example.com",
            "password": "123456789"
        }
    )
    data = response.get_json()
    
    assert response.status_code == 401  

    assert data["type"] == "errors/authentication-error"

