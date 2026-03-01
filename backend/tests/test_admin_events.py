from datetime import datetime

def test_admin_can_list_events(client, admin_token, many_events):
    
    res = client.get(
        "api/v1/admin/events?page=1&limit=10",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert res.status_code == 200

    data = res.get_json()
    assert "data" in data
    assert "events" in data["data"]
    assert len(data["data"]["events"]) == 10


def test_user_cannot_access_events(client, auth_token):
    
    res = client.get(
        "api/v1/admin/events?page=1&limit=10",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert res.status_code == 403


def test_admin_events_sorted_by_created_at_desc(client, admin_token, many_events):
    
    res = client.get(
        "api/v1/admin/events?page=1&limit=5&sort=created_at&order=desc&created_from=2020-01-01&created_to=2070-01-01",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    events = res.get_json()["data"]["events"]
    dates = [event["created_at"] for event in events]

    assert dates == sorted(dates, reverse=True)
    assert datetime.fromisoformat(dates[len(dates)-1]) >= datetime.strptime("2020-01-01T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") and datetime.fromisoformat(dates[0]) <= datetime.strptime("2070-01-01T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")


def test_admin_filter_by_entity_type(client, admin_token, many_events):
    
    res = client.get(
        "api/v1/admin/events?entity_type=task",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    events = res.get_json()["data"]["events"]

    assert all(event["entity_type"] == "task" for event in events)
