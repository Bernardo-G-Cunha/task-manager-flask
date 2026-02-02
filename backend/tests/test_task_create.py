from app.models import Task, Event
from app.extensions import db

def test_task_create(client, auth_token, tasks, app):
    
    payload = {
        "name": "Task add test",
        "description": "Task created to test create endpoint.",
        "tags": [{"name": "Tag add 1"}, {"name": "Tag add 2"}, {"name": "tag1"}]
    }

    response = client.post(
        f"/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json=payload
    )

    assert response.status_code == 201

    with app.app_context():
        task = Task.query.filter_by(name="Task add test").first()
        event = Event.query.filter_by(entity_id=task.id).first()
        assert task is not None
        assert event.event_type == "TASK_CREATED"

def test_error_task_create(client, auth_token, tasks, app):
    
    payload = {
        "description": "Error test.",
        "tags": [{"name": "Tag add 1"}, {"name": "Tag add 2"}]
    }

    response = client.post(
        f"/tasks/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json=payload
    )
    data = response.get_json()
    
    assert response.status_code == 422

    assert data["title"] == "Validation error"

    with app.app_context():
        task = Task.query.filter_by(description="Error test.").first()
        assert task is None
