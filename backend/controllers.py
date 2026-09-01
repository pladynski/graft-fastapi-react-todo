from typing import List

from schemas import TodoResponse, TodoCreate, TodoUpdate
from services import TodoService


class TodoController:
    """Controller class for todo API endpoints"""

    service = TodoService()

    @staticmethod
    def get_all_todos() -> List[TodoResponse]:
        """Get all todos"""
        return TodoController.service.get_all_todos()

    @staticmethod
    def get_todo(todo_id: int) -> TodoResponse:
        """Get a specific todo by ID"""
        return TodoController.service.get_todo_by_id(todo_id)

    @staticmethod
    def create_todo(todo: TodoCreate) -> TodoResponse:
        """Create a new todo"""
        return TodoController.service.create_todo(todo)

    @staticmethod
    def update_todo(todo_id: int, update: TodoUpdate) -> TodoResponse:
        """Update a todo's details"""
        return TodoController.service.update_todo(todo_id, update)

    @staticmethod
    def toggle_todo_completion(todo_id: int) -> TodoResponse:
        """Toggle a todo's completion status"""
        return TodoController.service.toggle_todo_completion(todo_id)

    @staticmethod
    def delete_todo(todo_id: int) -> str:
        """Delete a todo"""
        return TodoController.service.delete_todo(todo_id)["message"]
