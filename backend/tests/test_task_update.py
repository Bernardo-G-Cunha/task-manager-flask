from app.models.task import Task
from app.extensions import db

def test_task_update_success(client, auth_token, tasks, app):
    
    task_id = tasks[0]

    response = client.patch(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json={"name": "Task updated"}
    )

    assert response.status_code == 204
    
    with app.app_context():
        task = db.session.get(Task, task_id)

        assert task is not None
        assert task.name == "Task updated"

def test_error_task_update(client, auth_token, tasks, app):
    response = client.patch(
        "/tasks/5",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }, json={"name": "Task updated"}
    )

    data = response.get_json()
    
    assert response.status_code == 404
    
    assert data["title"] == 'Task Not Found'