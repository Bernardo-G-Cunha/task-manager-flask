def test_task_delete(client, auth_token, tasks):
    response = client.delete(
        "/tasks/1",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 204


def test_error_task_delete(client, auth_token, tasks):
    response = client.delete(
        "/tasks/6",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 404