from app.extensions import db
from app.models import Event

def create_event(
    *,
    entity_type: str,
    entity_id: int,
    event_type: str,
    actor_user_id: int | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
):
    event = Event(
        entity_type=entity_type,
        entity_id=entity_id,
        event_type=event_type,
        actor_user_id=actor_user_id,
        old_value=old_value,
        new_value=new_value,
    )
    db.session.add(event)
