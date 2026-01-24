from app.models.task import Task
from app.extensions import db

def test_task_delete(client, auth_token, tasks, app):

    task_id = tasks[0]
    
    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 204

    with app.app_context():
        task = db.session.get(Task, task_id)

        assert task is None


def test_error_task_delete(client, auth_token, tasks):
    response = client.delete(
        "/tasks/6",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 404