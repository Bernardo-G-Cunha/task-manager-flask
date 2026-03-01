from datetime import datetime

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


def test_admin_creation_sort_filter(client, admin_token, many_tasks):
    res = client.get("api/v1/admin/tasks?page=1&limit=11&sort=creation_date&order=asc&created_from=2020-01-01&created_to=2070-01-01", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    data = res.get_json()

    dates = [task["creation_date"] for task in data["data"]["tasks"]]
    assert dates == sorted(dates, reverse=False)
    assert datetime.fromisoformat(dates[0]) >= datetime.strptime("2020-01-01T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") and datetime.fromisoformat(dates[len(dates)-1]) <= datetime.strptime("2070-01-01T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    assert data["pagination"]["limit"] == 11
    assert data["pagination"]["page"] == 1
    assert res.status_code == 200
