def test_task_update_success(client, auth_token, tasks):
    response = client.patch(
        "/tasks/1",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json={"name": "Task updated"}
    )
    
    assert response.status_code == 204
    

def test_erro_task_update(client, auth_token, tasks):
    response = client.patch(
        "/tasks/5",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json={"name": "Task updated"}
    )

    data = response.get_json()
    
    assert response.status_code == 404
    
    assert data["title"] == 'Task Not Found'