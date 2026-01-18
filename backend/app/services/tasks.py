from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app.schemas.user_schema import *
from app.exceptions.auth_exceptions import *
from app.dtos.dto_task import TaskCreateDTO
from sqlalchemy.exc import IntegrityError, OperationalError


def create_task(task_data: TaskCreateDTO, user_id: int) -> None:
    new_task = Task(**task_data, user_id=user_id)
    
    try:
        db.session.add(new_task)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        raise OperationalError() from e

