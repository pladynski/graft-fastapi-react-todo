# Graftcode: TestClient, URLs, and status-code asserts replaced with TodoController.method(...) calls.
# Benefit: ordinary unit tests — no HTTP client, no 404/200 mapping.
# https://graftcode.com · https://github.com/grft-dev/graftcode · https://docs.graftcode.com

import pytest
from models import Todo
from controllers import TodoController
from schemas import TodoCreate, TodoUpdate
from repositories import TodoNotFoundException


@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Reset database before each test"""
    from models import Todo, db
    
    # Ensure we're connected
    if db.is_closed():
        db.connect()
    
    # Drop and recreate tables to start fresh
    db.drop_tables([Todo], safe=True)
    db.create_tables([Todo])
    
    yield db
    
    # Clean up after test
    db.drop_tables([Todo], safe=True)


@pytest.fixture
def setup_todos():
    """Setup initial test todos using Peewee directly"""
    Todo.create(title="Buy groceries", description="Milk, bread, eggs", completed=False)
    Todo.create(title="Write tests", description="Unit tests for todo API", completed=True)
    return [
        {"title": "Buy groceries", "description": "Milk, bread, eggs", "completed": False},
        {"title": "Write tests", "description": "Unit tests for todo API", "completed": True}
    ]


def test_get_all_todos_empty():
    """Test getting all todos when none exist"""
    todos = TodoController.get_all_todos()
    assert todos == []


def test_create_todo():
    """Test creating a new todo"""
    data = TodoController.create_todo(TodoCreate(title="Learn FastAPI", description="Build a todo app"))
    assert data.title == "Learn FastAPI"
    assert data.description == "Build a todo app"
    assert data.completed == False


def test_get_all_todos(setup_todos):
    """Test getting all todos"""
    data = TodoController.get_all_todos()
    assert len(data) == 2

    # Verify todo titles
    todo_titles = [t.title for t in data]
    assert "Buy groceries" in todo_titles
    assert "Write tests" in todo_titles


def test_get_todo(setup_todos):
    """Test getting a specific todo"""
    # First create a todo to get its ID
    todo = Todo.create(title="Test todo", description="For testing", completed=False)
    
    data = TodoController.get_todo(todo.id)
    assert data.title == "Test todo"
    assert data.description == "For testing"
    assert data.completed == False


def test_update_todo(setup_todos):
    """Test updating a todo"""
    # First create a todo to update
    todo = Todo.create(title="Original title", description="Original desc", completed=False)
    
    data = TodoController.update_todo(
        todo.id,
        TodoUpdate(title="Updated title", description="Updated desc", completed=True),
    )
    assert data.title == "Updated title"
    assert data.description == "Updated desc"
    assert data.completed == True


def test_partial_update_todo():
    """Test partial updating a todo"""
    # Create a todo first
    todo = Todo.create(title="Original title", description="Original desc", completed=False)
    
    # Update only the completed status
    data = TodoController.update_todo(todo.id, TodoUpdate(completed=True))
    assert data.title == "Original title"  # Should remain unchanged
    assert data.description == "Original desc"  # Should remain unchanged
    assert data.completed == True  # Should be updated


def test_toggle_todo_completion():
    """Test toggling a todo's completion status"""
    # Create a todo first
    todo = Todo.create(title="Toggle test", description="Test toggle", completed=False)
    
    # Toggle to completed
    data = TodoController.toggle_todo_completion(todo.id)
    assert data.completed == True
    
    # Toggle back to not completed
    data = TodoController.toggle_todo_completion(todo.id)
    assert data.completed == False


def test_delete_todo(setup_todos):
    """Test deleting a todo"""
    # Create a todo to delete
    todo = Todo.create(title="To be deleted", description="Will be removed", completed=False)
    
    message = TodoController.delete_todo(todo.id)
    assert "deleted" in message

    # Verify todo is deleted
    with pytest.raises(TodoNotFoundException):
        TodoController.get_todo(todo.id)


def test_todo_not_found():
    """Test operations on non-existent todo"""
    with pytest.raises(TodoNotFoundException):
        TodoController.get_todo(999)

    with pytest.raises(TodoNotFoundException):
        TodoController.update_todo(999, TodoUpdate(title="Updated"))

    with pytest.raises(TodoNotFoundException):
        TodoController.toggle_todo_completion(999)

    with pytest.raises(TodoNotFoundException):
        TodoController.delete_todo(999)


def test_create_todo_minimal():
    """Test creating a todo with minimal data"""
    data = TodoController.create_todo(TodoCreate(title="Minimal todo"))
    assert data.title == "Minimal todo"
    assert data.description == ""  # Should default to empty string
    assert data.completed == False  # Should default to False


def test_complex_workflow():
    """Test a complex workflow with multiple operations"""
    # Create todo
    created = TodoController.create_todo(TodoCreate(title="Workflow todo", description="Testing workflow"))
    todo_id = created.id

    # Update description
    data = TodoController.update_todo(todo_id, TodoUpdate(description="Updated description"))
    assert data.description == "Updated description"
    assert data.title == "Workflow todo"  # Should remain unchanged

    # Toggle completion
    data = TodoController.toggle_todo_completion(todo_id)
    assert data.completed == True

    # Update title while keeping completion status
    data = TodoController.update_todo(todo_id, TodoUpdate(title="Final title"))
    assert data.title == "Final title"
    assert data.completed == True  # Should remain True

    # Delete
    TodoController.delete_todo(todo_id)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
