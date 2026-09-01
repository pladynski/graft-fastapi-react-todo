from dataclasses import dataclass
from typing import Optional

@dataclass
class TodoResponse:
    id: int = 0
    title: str = ""
    description: str = ""
    completed: bool = False

    @classmethod
    def model_validate(cls, todo, from_attributes=True):
        return cls(id=todo.id, title=todo.title, description=todo.description, completed=todo.completed)

@dataclass
class TodoCreate:
    title: str = ""
    description: Optional[str] = ''

@dataclass
class TodoUpdate:
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
