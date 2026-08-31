import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent / "todoservice"))

from todo_service import TodoService, _reset_for_tests


@pytest.fixture(scope="function", autouse=True)
def isolated_db():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    _reset_for_tests(path)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


def test_list_todos_empty():
    assert TodoService.list_todos() == []


def test_create_todo():
    todo = TodoService.create_todo("Learn Graftcode", "Build a todo app")
    assert todo[1] == "Learn Graftcode"
    assert todo[2] == "Build a todo app"
    assert todo[3] == "false"
    assert isinstance(todo[0], str)
    assert todo[0] != ""


def test_create_todo_minimal():
    todo = TodoService.create_todo("Minimal todo", "")
    assert todo[1] == "Minimal todo"
    assert todo[2] == ""
    assert todo[3] == "false"


def test_list_todos():
    TodoService.create_todo("Buy groceries", "Milk, bread, eggs")
    TodoService.create_todo("Write tests", "Unit tests for todo service")
    snapshot = TodoService.list_todos()
    assert len(snapshot) == 8
    titles = [snapshot[i] for i in range(1, len(snapshot), 4)]
    assert "Buy groceries" in titles
    assert "Write tests" in titles


def test_get_todo():
    created = TodoService.create_todo("Test todo", "For testing")
    todo = TodoService.get_todo(created[0])
    assert todo[1] == "Test todo"
    assert todo[2] == "For testing"
    assert todo[3] == "false"


def test_update_todo():
    created = TodoService.create_todo("Original title", "Original desc")
    updated = TodoService.update_todo(created[0], "Updated title", "Updated desc")
    assert updated[1] == "Updated title"
    assert updated[2] == "Updated desc"
    assert updated[3] == "false"


def test_toggle_todo():
    created = TodoService.create_todo("Toggle test", "Test toggle")
    completed = TodoService.toggle_todo(created[0])
    assert completed[3] == "true"
    incomplete = TodoService.toggle_todo(created[0])
    assert incomplete[3] == "false"


def test_delete_todo():
    created = TodoService.create_todo("To be deleted", "Will be removed")
    assert TodoService.delete_todo(created[0]) is True
    with pytest.raises(Exception, match="not found"):
        TodoService.get_todo(created[0])


def test_todo_not_found():
    with pytest.raises(Exception, match="not found"):
        TodoService.get_todo("999")
    with pytest.raises(Exception, match="not found"):
        TodoService.update_todo("999", "Updated", "")
    with pytest.raises(Exception, match="not found"):
        TodoService.toggle_todo("999")
    with pytest.raises(Exception, match="not found"):
        TodoService.delete_todo("999")


def test_complex_workflow():
    created = TodoService.create_todo("Workflow todo", "Testing workflow")
    todo_id = created[0]

    updated = TodoService.update_todo(todo_id, created[1], "Updated description")
    assert updated[2] == "Updated description"
    assert updated[1] == "Workflow todo"

    toggled = TodoService.toggle_todo(todo_id)
    assert toggled[3] == "true"

    renamed = TodoService.update_todo(todo_id, "Final title", toggled[2])
    assert renamed[1] == "Final title"
    assert renamed[3] == "true"

    assert TodoService.delete_todo(todo_id) is True
