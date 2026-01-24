def test_task_view(client, auth_token, tasks):
    response = client.get(
        "/tasks/1",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    data = response.get_json()
    
    assert response.status_code == 200

    assert data["data"]["task"]["id"] == 1
    
def test_error_task_view(client, auth_token, tasks):
    response = client.get(
        "/tasks/6",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    
    assert response.status_code == 404
