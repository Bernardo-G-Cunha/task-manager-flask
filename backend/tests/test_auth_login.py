def test_login_success(client, user):
    response_login = client.post(
        "/auth/",
        json={
            "email": "test@example.com",
            "password": "123456789"
        }
    )
    
    assert response_login.status_code == 200
    data = response_login.get_json()
    assert "access_token" in data


def test_login_authentication_error(client, user):
    response_login = client.post(
        "/auth/",
        json={
            "email": "false@example.com",
            "password": "123456789"
        }
    )

    assert response_login.status_code == 401  
    data = response_login.get_json()
    assert data["type"] == "errors/authentication-error"

