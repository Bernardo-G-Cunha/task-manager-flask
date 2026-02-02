from app.extensions import db
from app.models import Task, User, Event
from app.schemas import task_list_schema, user_list_schema, event_list_schema
from app.dtos import PaginatedResultDTO
from sqlalchemy import desc, asc
from sqlalchemy.orm import joinedload

def get_all_tasks(*, page: int, limit: int, sort: str, order: str, filters: dict) -> PaginatedResultDTO:

    offset = (page - 1) * limit

    column_map = {
        "created_at": Task.creation_date,
        "name": Task.name,
        "done": Task.done
    }

    sort_column = column_map.get(sort, Task.creation_date)
    direction = desc if order == "desc" else asc

    query = Task.query.options(joinedload(Task.tags))

    if "done" in filters:
        query = query.filter(Task.done == (filters["done"] == "true"))

    if "id" in filters:
        query = query.filter(Task.id == int(filters["id"]))

    if "name" in filters:
        query = query.filter(Task.name.ilike(f"%{filters['name']}%"))

    total = query.count()

    tasks = (
        query
        .order_by(direction(sort_column))
        .limit(limit)
        .offset(offset)
        .all()
    )

    return PaginatedResultDTO(
        items=task_list_schema.dump(tasks),
        page=page,
        limit=limit,
        total=total
    )

def get_all_users(*, page: int, limit: int, sort: str, order: str, filters: dict) -> PaginatedResultDTO:

    offset = (page - 1) * limit

    column_map = {
        "email": User.email,
        "username": User.username,
    }

    sort_column = column_map.get(sort, User.username)
    direction = desc if order == "desc" else asc

    query = User.query

    if "email" in filters:
        query = query.filter(User.email == (filters["email"]))

    if "id" in filters:
        query = query.filter(User.id == int(filters["id"]))

    if "username" in filters:
        query = query.filter(User.username.ilike(f"%{filters['username']}%"))

    total = query.count()

    users = (
        query
        .order_by(direction(sort_column))
        .limit(limit)
        .offset(offset)
        .all()
    )

    return PaginatedResultDTO(
        items=user_list_schema.dump(users),
        page=page,
        limit=limit,
        total=total
    )

def get_events(*, page: int, limit: int, sort: str, order: str, filters: dict) -> PaginatedResultDTO:
    
    offset = (page - 1) * limit

    column_map = {
        "entity_type": Event.entity_type,
        "entity_id": Event.entity_id,
        "event_type": Event.event_type,
        "actor_user_id": Event.actor_user_id,
        "created_at": Event.created_at
    }

    sort_column = column_map.get(sort, Event.created_at)
    direction = desc if order == "desc" else asc

    query = Event.query

    if filters.get("entity_type"):
        query = query.filter(Event.entity_type == filters["entity_type"])

    if filters.get("entity_id"):
        query = query.filter(Event.entity_id == int(filters["entity_id"]))

    if filters.get("event_type"):
        query = query.filter(Event.event_type == filters["event_type"])

    if filters.get("actor_user_id"):
        query = query.filter(Event.actor_user_id == int(filters["actor_user_id"]))

    if filters.get("from"):
        query = query.filter(Event.created_at >= filters["from"])

    if filters.get("to"):
        query = query.filter(Event.created_at <= filters["to"])

    total = query.count()

    events = (
        query
        .order_by(direction(sort_column))
        .limit(limit)
        .offset(offset)
        .all()
    )

    return PaginatedResultDTO(
        items=event_list_schema.dump(events),
        page=page,
        limit=limit,
        total=total
    )