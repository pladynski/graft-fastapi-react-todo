import os

os.environ["APP_ENV"] = "test"

import pytest

from controllers import TodoController
from models import Todo, db
from repositories import TodoNotFoundException


@pytest.fixture(scope="function", autouse=True)
def test_db():
    if db.is_closed():
        db.connect()
    db.drop_tables([Todo], safe=True)
    db.create_tables([Todo])
    yield db
    db.drop_tables([Todo], safe=True)


def test_get_all_todos_empty():
    assert TodoController.get_all_todos() == []


def test_create_todo():
    todo = TodoController.create_todo("Learn Graftcode", "Build a todo app")
    assert todo.title == "Learn Graftcode"
    assert todo.description == "Build a todo app"
    assert todo.completed is False


def test_create_todo_minimal():
    todo = TodoController.create_todo("Minimal todo", "")
    assert todo.title == "Minimal todo"
    assert todo.description == ""
    assert todo.completed is False


def test_get_all_todos():
    TodoController.create_todo("Buy groceries", "Milk, bread, eggs")
    TodoController.create_todo("Write tests", "Unit tests")
    todos = TodoController.get_all_todos()
    assert len(todos) == 2
    titles = [t.title for t in todos]
    assert "Buy groceries" in titles
    assert "Write tests" in titles


def test_get_todo():
    created = TodoController.create_todo("Test todo", "For testing")
    todo = TodoController.get_todo(created.id)
    assert todo.title == "Test todo"
    assert todo.description == "For testing"


def test_update_todo():
    created = TodoController.create_todo("Original title", "Original desc")
    updated = TodoController.update_todo(created.id, "Updated title", "Updated desc")
    assert updated.title == "Updated title"
    assert updated.description == "Updated desc"


def test_toggle_todo_completion():
    created = TodoController.create_todo("Toggle test", "Test toggle")
    completed = TodoController.toggle_todo_completion(created.id)
    assert completed.completed is True
    incomplete = TodoController.toggle_todo_completion(created.id)
    assert incomplete.completed is False


def test_delete_todo():
    created = TodoController.create_todo("To be deleted", "Will be removed")
    message = TodoController.delete_todo(created.id)
    assert "deleted" in message
    with pytest.raises(TodoNotFoundException):
        TodoController.get_todo(created.id)


def test_todo_not_found():
    with pytest.raises(TodoNotFoundException):
        TodoController.get_todo(999)
    with pytest.raises(TodoNotFoundException):
        TodoController.update_todo(999, "Updated", "")
    with pytest.raises(TodoNotFoundException):
        TodoController.toggle_todo_completion(999)
    with pytest.raises(TodoNotFoundException):
        TodoController.delete_todo(999)
