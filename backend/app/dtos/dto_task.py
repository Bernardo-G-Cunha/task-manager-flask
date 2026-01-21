from dataclasses import dataclass
from datetime import datetime

@dataclass
class TaskCreateDTO:
    user_id: int
    name: str
    description: str
    due_date: str
    tags: list[str]
    done: bool = False
   

@dataclass
class TaskGetDTO:
    name: str
    description: str
    due_date: str
    done: bool
    creation_date: str
    tags: list[str]

@dataclass
class TaskUpdateDTO:
    id: int
    name: str
    description: str
    due_date: str
    done: bool
    tags: list[str]