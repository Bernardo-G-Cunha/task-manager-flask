def test_tasks_default_pagination(client, auth_token, many_tasks):

    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]["tasks"]) == 10
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["limit"] == 10
    assert data["pagination"]["total"] == 30


def test_tasks_empty_page(client, auth_token, many_tasks):

    response = client.get(
        "/tasks?page=4&limit=10",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["data"]["tasks"] == []


def test_tasks_order_pagination(client, auth_token, many_tasks):

    response = client.get(
        "/tasks?page=1&limit=10&sort=name&order=asc",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    data = response.get_json()

    names = [task["name"] for task in data["data"]["tasks"]]

    assert response.status_code == 200
    assert names == sorted(names)


def test_error_get_tasks(client, auth_token, many_tasks):
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token + 'E'}"
        }
    )
    data = response.get_json()

    assert response.status_code == 401

    assert data['title'] == 'Invalid token'
