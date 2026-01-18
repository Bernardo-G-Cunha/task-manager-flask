def test_get_tasks(client, auth_token, tasks):
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    
    assert len(data["data"]["tasks"]) == 2
    assert data["data"]["tasks"][0]["name"] == "Test task 1"


def test_error_get_tasks(client, auth_token, tasks):
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token + 'E'}"
        }
    )
    data = response.get_json()

    assert response.status_code == 401

    assert data['title'] == 'Invalid token'
