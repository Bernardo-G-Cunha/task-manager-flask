from app.extensions import db
from app.models.task import Task
from app.exceptions import TaskNotFoundError
from app.dtos.dto_task import TaskCreateDTO, TaskUpdateDTO, TaskGetDTO
from app.schemas.task_schema import task_complete_schema
from sqlalchemy.exc import IntegrityError


def add_task(task_data: TaskCreateDTO, user_id: int) -> None:
    
    data = task_data.__dict__.copy()

    tags = data.pop("tags", None)
    
    new_task = Task(**data, user_id=user_id)

    if tags:
        new_task.tags.extend(tags)
    
    try:
        db.session.add(new_task)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise

def find_task(task_id: int, user_id: int) -> TaskGetDTO:

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if task is None:
        raise TaskNotFoundError()
    
    taskDTO = task_complete_schema.dump(task)

    return taskDTO

def update_task(update_task_data: TaskUpdateDTO, user_id: int, task_id: int) -> None:
    
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        raise TaskNotFoundError()

    for field, value in update_task_data.__dict__.items():
        if value is not None and field != "id":
            setattr(task, field, value)

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise

def remove_task(task_id: int, user_id: int) -> None:

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        raise TaskNotFoundError()
    
    try:
        db.session.delete(task)
        db.session.commit()
    
    except IntegrityError:
        db.session.rollback()
        raise
