def test_signup_sucesso(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "bernardo",
            "email": "bernardo@email.com",
            "password": "teste_8_caracteres"
        }
    )
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    
    assert data["message"] == "Successfully signed up"


def test_signup_dados_invalidos(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "email-sem-username"
            # faltam campos obrigatórios
        }
    )

    assert response.status_code == 422


def test_signup_usuario_duplicado(client):
    payload = {
        "username": "bernardo",
        "email": "bernardo@email.com",
        "password": "123456rervef"
    }

    client.post("/auth/signup", json=payload)
    response = client.post("/auth/signup", json=payload)

    assert response.status_code == 409
