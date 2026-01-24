from dataclasses import dataclass

@dataclass
class TaskCompleteDTO:
    id: int
    user_id: int
    name: str
    description: str
    due_date: str
    done: bool
    creation_date: str
    tags: list[str]


@dataclass
class TaskCreateDTO:
    name: str
    description: str | None = None
    due_date: str | None = None
    tags: list[str] | None = None
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
    name: str | None = None
    description: str | None = None
    due_date: str | None = None
    done: bool | None = None
    tags: list[str] | None = None