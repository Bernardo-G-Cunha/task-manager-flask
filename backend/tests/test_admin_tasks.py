def test_admin_access_denied(client, auth_token):
    res = client.get("api/v1/admin/tasks", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert res.status_code == 403


def test_admin_name_filter(client, admin_token, many_tasks):
    res = client.get("api/v1/admin/tasks?page=1&limit=10&name=Task%2012", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()

    assert data["data"]["tasks"][0]["name"] == "Task 12"
    assert res.status_code == 200


def test_admin_done_filter(client, admin_token, many_tasks):
    res = client.get("api/v1/admin/tasks?page=2&limit=10&done=true", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()

    assert str(data["data"]["tasks"][0]["done"]) == "True"    
    assert res.status_code == 200


def test_admin_creation_sort(client, admin_token, many_tasks):
    res = client.get("api/v1/admin/tasks?page=2&limit=11&sort=creation_date&order=asc", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()
    
    assert data["data"]["tasks"][2]["creation_date"] < data["data"]["tasks"][3]["creation_date"]
    assert data["pagination"]["limit"] == 11
    assert data["pagination"]["page"] == 2
    assert res.status_code == 200
