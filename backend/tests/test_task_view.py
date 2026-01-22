def test_task_view(client, auth_token, tasks):
    response = client.get(
        "/tasks/1",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    