from dataclasses import dataclass
from typing import Optional

@dataclass
class EventDTO:
    id: int
    entity_type: str
    entity_id: int
    event_type: str
    actor_user_id: Optional[int]
    old_value: dict | None
    new_value: dict | None
    created_at: str