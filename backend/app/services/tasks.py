from app.extensions import db
from app.models.task import Task
from app.models.tag import Tag
from app.exceptions import TaskNotFoundError
from app.dtos.dto_task import TaskCreateDTO, TaskUpdateDTO, TaskGetDTO
from app.schemas.task_schema import task_complete_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
from sqlalchemy.orm import joinedload

def get_or_create_tags(tag_names: list[str]) -> list[int]:

    if not tag_names:
        return []

    normalized = list(
        set(tag.name.strip().lower() for tag in tag_names)
    )

    if not normalized:
        return []

    existing = (
        db.session.query(Tag)
        .filter(Tag.name.in_(normalized))
    ).all()

    existing_map = {tag.name: tag.id for tag in existing}

    tag_ids = []

    for name in normalized:
        if name in existing_map:
            tag_ids.append(existing_map[name])
        else:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.flush()
            tag_ids.append(tag.id)

    return tag_ids


def add_task(task_data: TaskCreateDTO, user_id: int) -> None:

    data = task_data.__dict__.copy()
    tags = data.pop("tags", None)
    new_task = Task(**data, user_id=user_id)

    db.session.add(new_task)
    db.session.flush()

    tag_ids = get_or_create_tags(tags)

    tags = (
        db.session.query(Tag)
        .filter(Tag.id.in_(tag_ids))
        .all()
    )

    new_task.tags = tags

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise

def get_tasks_paginated(user_id: int, page: int, limit: int, sort: str, order: str):
    
    offset = (page - 1) * limit

    column_map = {
        "created_at": Task.creation_date,
        "name": Task.name,
        "done": Task.done
    }

    sort_column = column_map.get(sort, Task.creation_date)
    direction = desc if order == "desc" else asc

    query = (
        db.session.query(Task)
        .options(joinedload(Task.tags))
        .filter(Task.user_id == user_id)
        .order_by(direction(sort_column))
        .limit(limit)
        .offset(offset)
    )

    tasks = query.all()

    total = (
        db.session.query(Task)
        .filter(Task.user_id == user_id)
        .count()
    )

    return tasks, total


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

    data = update_task_data.__dict__.copy()

    tags_field = data.pop("tags", None)

    for field, value in data.items():
        if value is not None and field != "id" and field != "user_id":
            setattr(task, field, value)
    
    if tags_field is not None:
        tag_ids = get_or_create_tags(tags_field)
        
        tags = (
            db.session.query(Tag)
            .filter(Tag.id.in_(tag_ids))
            .all()
        )

        task.tags = tags

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
