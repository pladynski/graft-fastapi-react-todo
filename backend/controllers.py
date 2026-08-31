"""Graftcode public surface. Delegates to the existing TodoService."""

from schemas import TodoCreate, TodoResponse, TodoUpdate


def _service():
    # Imported lazily so Graftcode module analysis does not load peewee.
    from services import TodoService

    return TodoService()


def _ensure_db() -> None:
    # Replaces the old FastAPI lifespan table-create. Same models/db as before.
    from models import Todo, db

    if db.is_closed():
        db.connect()
    db.create_tables([Todo], safe=True)


class TodoController:
    """Thin facade: same operations as the old HTTP controller, no FastAPI."""

    @staticmethod
    def get_all_todos() -> list[TodoResponse]:
        _ensure_db()
        return _service().get_all_todos()

    @staticmethod
    def get_todo(todo_id: int) -> TodoResponse:
        _ensure_db()
        return _service().get_todo_by_id(todo_id)

    @staticmethod
    def create_todo(title: str, description: str) -> TodoResponse:
        _ensure_db()
        return _service().create_todo(TodoCreate(title=title, description=description))

    @staticmethod
    def update_todo(todo_id: int, title: str, description: str) -> TodoResponse:
        _ensure_db()
        return _service().update_todo(todo_id, TodoUpdate(title=title, description=description))

    @staticmethod
    def toggle_todo_completion(todo_id: int) -> TodoResponse:
        _ensure_db()
        return _service().toggle_todo_completion(todo_id)

    @staticmethod
    def delete_todo(todo_id: int) -> str:
        _ensure_db()
        result = _service().delete_todo(todo_id)
        return result["message"]
