from fastapi.testclient import TestClient
import pytest
import requests

# Prep to import the app fastapi object and create a test client
import sys
from pathlib import Path

# *\ Import to Get SQLLCHEMY Base class for DB Schema Creation and Migrations
# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent))

# Now you can use relative imports
from api.index import app

client = TestClient(app)

# Test integration and interaction of your FastAPI application with the database and service layer.

# A pytest fixture to get bearer token
@pytest.fixture
def bearer():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://localhost:8000/api/auth/login",
        data=login_data
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# Test to get all todos
def test_read_all_todos(bearer):
    response = client.get(
        "api/todos/",
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert response.status_code == 200


# Test to create a todo
def test_todo_creation_in_database(bearer):
    todo_data = {
        "title": "Test TODO",
        "description": "Test TODO Description",
        "completed": False
    }
    response = client.post(
        "/api/todos/",
        json=todo_data,
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test TODO"
    assert data["description"] == "Test TODO Description"
    assert data["completed"] == False

    # Cleanup
    client.delete(f"/api/todos/{data['id']}", headers={"Authorization": f"Bearer {bearer}"})

# Test to get todo by id
def test_todo_retrival_db_by_id(bearer):
    # Create a todo
    create_response = client.post(
        "/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {bearer}"}
    )
    todo_id = create_response.json()["id"]

    # Get the todo by its ID
    response = client.get(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

    # Cleanup
    client.delete(f"/api/todos/{todo_id}", headers={"Authorization": f"Bearer {bearer}"})

# Test to update a todo
def test_todo_update_in_db(bearer):
    # Create a todo
    create_response = client.post(
        "/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {bearer}"}
    )
    todo_id = create_response.json()["id"]

    # Update the todo
    update_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "title": "Updated TODO",
            "description": "Updated TODO Description",
            "completed": True
        },
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert update_response.status_code == 200

    # Cleanup
    client.delete(f"/api/todos/{todo_id}", headers={"Authorization": f"Bearer {bearer}"})

# Test to delete a todo
def test_db_delete_todo(bearer):
    # Create a todo
    create_response = client.post(
        "/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {bearer}"}
    )
    todo_id = create_response.json()["id"]

    # Delete the todo
    delete_response = client.delete(
        f"/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert delete_response.status_code == 200
