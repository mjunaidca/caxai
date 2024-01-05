import requests
from fastapi.testclient import TestClient
from ...main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_todo():
    response = requests.post(
        "http://localhost:8000/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test TODO"
    assert response.json()["description"] == "Test TODO Description"
    assert response.json()["completed"] == False

def test_get_todos():
    response = requests.get("http://localhost:8000/api/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo_by_id():
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    todo_id = response.json()["id"]

    # Get the todo by its ID
    response = requests.get(f"http://localhost:8000/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Test TODO"
    assert response.json()["description"] == "Test TODO Description"
    assert response.json()["completed"] == False

    # Cleanup
    requests.delete(f"http://localhost:8000/api/todos/{todo_id}")

def test_update_todo():
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    todo_id = response.json()["id"]

    # Update the todo
    response = requests.put(
        f"http://localhost:8000/api/todos/{todo_id}",
        json={
            "title": "Updated TODO",
            "description": "Updated TODO Description",
            "completed": True
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Updated TODO"
    assert response.json()["description"] == "Updated TODO Description"
    assert response.json()["completed"] == True

    # Cleanup
    requests.delete(f"http://localhost:8000/api/todos/{todo_id}")

def test_delete_todo():
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    todo_id = response.json()["id"]

    # Delete the todo
    response = requests.delete(f"http://localhost:8000/api/todos/{todo_id}")
    assert response.status_code == 200

    # Try to get the deleted todo
    response = requests.get(f"http://localhost:8000/api/todos/{todo_id}")
    assert response.status_code == 404