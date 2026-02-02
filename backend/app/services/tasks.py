from app.extensions import db
from app.models import Task, Tag
from app.services.events import create_event
from app.exceptions import TaskNotFoundError
from app.dtos import TaskCreateDTO, TaskUpdateDTO, TaskCompleteDTO, PaginatedResultDTO
from app.schemas import task_complete_schema, task_list_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone

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

    create_event(
        entity_type="task",
        entity_id=new_task.id,
        event_type="TASK_CREATED",
        actor_user_id=user_id,
        new_value={
            "name": new_task.name,
            "done": new_task.done,
            "description": str(new_task.description) if new_task.description else None,
            "due_date": str(new_task.due_date) if new_task.due_date else None
        }
    )

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
        .filter(Task.user_id == user_id, Task.deleted_at.is_(None))
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

    return PaginatedResultDTO(
        items=task_list_schema.dump(tasks),
        page=page,
        limit=limit,
        total=total
    )


def find_task(task_id: int, user_id: int) -> TaskCompleteDTO:

    task = Task.query.filter_by(id=task_id, user_id=user_id, deleted_at=None).first()
    
    if task is None:
        raise TaskNotFoundError()
    
    data = task_complete_schema.dump(task)
    
    return TaskCompleteDTO(**data)

def update_task(update_task_data: TaskUpdateDTO, user_id: int, task_id: int) -> None:
    
    task = Task.query.filter_by(id=task_id, user_id=user_id, deleted_at=None).first()
    
    if not task:
        raise TaskNotFoundError()

    old_state = {
        "name": task.name,
        "description": str(task.description) if task.description else None,
        "done": task.done,
        "due_date": str(task.due_date) if task.due_date else None,
    }

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

    new_state = {
        "name": task.name,
        "description": str(task.description) if task.description else None,
        "done": task.done,
        "due_date": str(task.due_date) if task.due_date else None,
    }

    event_type = "TASK_COMPLETED" if (
        old_state["done"] is False and new_state["done"] is True
    ) else "TASK_UPDATED"

    create_event(
        entity_type="task",
        entity_id=task.id,
        event_type=event_type,
        actor_user_id=user_id,
        old_value=old_state,
        new_value=new_state,
    )

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        raise


def remove_task(task_id: int, user_id: int) -> None:

    task = Task.query.filter_by(id=task_id, user_id=user_id, deleted_at=None).first()

    if not task:
        raise TaskNotFoundError()

    task.deleted_at = datetime.now(timezone.utc)

    create_event(
        entity_type="task",
        entity_id=task.id,
        event_type="TASK_DELETED",
        actor_user_id=user_id,
        old_value={
            "name": task.name,
            "done": task.done,
        }
    )

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
