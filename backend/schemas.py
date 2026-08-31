from dataclasses import dataclass


@dataclass
class TodoResponse:
    id: int
    title: str
    description: str
    completed: bool


@dataclass
class TodoCreate:
    title: str
    description: str = ""


@dataclass
class TodoUpdate:
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
