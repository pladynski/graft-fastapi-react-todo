# Graftcode: stripped FastAPI and HTTPException. Same method names stay a thin facade over TodoService — that is the graft contract.
# Benefit: no HTTP plumbing in this file; this surface is MCP-ready (copy the MCP config from Graftcode Vision).
# https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

from typing import List

from schemas import TodoResponse, TodoCreate, TodoUpdate
from services import TodoService

_service = TodoService()


class TodoController:
    """Controller class for todo API endpoints"""

    @staticmethod
    def get_all_todos() -> List[TodoResponse]:
        """Get all todos"""
        return _service.get_all_todos()

    @staticmethod
    def get_todo(todo_id: int) -> TodoResponse:
        """Get a specific todo by ID"""
        return _service.get_todo_by_id(todo_id)

    @staticmethod
    def create_todo(todo: TodoCreate) -> TodoResponse:
        """Create a new todo"""
        return _service.create_todo(todo)

    @staticmethod
    def update_todo(todo_id: int, update: TodoUpdate) -> TodoResponse:
        """Update a todo's details"""
        return _service.update_todo(todo_id, update)

    @staticmethod
    def toggle_todo_completion(todo_id: int) -> TodoResponse:
        """Toggle a todo's completion status"""
        return _service.toggle_todo_completion(todo_id)

    @staticmethod
    def delete_todo(todo_id: int) -> str:
        """Delete a todo"""
        return _service.delete_todo(todo_id)["message"]
