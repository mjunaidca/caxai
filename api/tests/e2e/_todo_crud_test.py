
import requests
import pytest

# A pytest fixture to get bearer


@pytest.fixture
def bearer():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/login",
        data=login_data  # Send as form data
    )
    assert response.status_code == 200
    return response.json()["access_token"]


# a get test with invalid bearer token
def test_get_todos_with_invalid_token():
    response = requests.get(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": "Bearer <YOUR_GithubPersonalAccessToken_HERE>"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}

# a get test without bearer token
def test_get_todos_without_token():
    response = requests.get(
        "http://localhost:8000/api/todos/",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

#  test with valid bearer token that comes from fixture
def test_get_todos_with_valid_token(bearer):
    response = requests.get(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": f"Bearer {bearer}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_create_todo(bearer):
    response = requests.post(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": f"Bearer {bearer}"},
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test TODO"
    assert response.json()["description"] == "Test TODO Description"
    assert response.json()["completed"] == False

    todo_id = response.json()["id"]

    # Cleanup
    requests.delete(
        f"http://localhost:8000/api/todos/{todo_id}", headers={"Authorization": f"Bearer {bearer}"})


def test_get_todo_by_id(bearer):
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": f"Bearer {bearer}"},
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    todo_id = response.json()["id"]

    # Get the todo by its ID
    response = requests.get(f"http://localhost:8000/api/todos/{todo_id}",
                            headers={"Authorization": f"Bearer {bearer}"})
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Test TODO"
    assert response.json()["description"] == "Test TODO Description"
    assert response.json()["completed"] == False

    # Cleanup
    requests.delete(
        f"http://localhost:8000/api/todos/{todo_id}", headers={"Authorization": f"Bearer {bearer}"})


def test_update_todo(bearer):
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": f"Bearer {bearer}"},
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
        headers={"Authorization": f"Bearer {bearer}"},
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
    requests.delete(f"http://localhost:8000/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {bearer}"})


def test_delete_todo(bearer):
    # Create a todo
    response = requests.post(
        "http://localhost:8000/api/todos/",
        headers={"Authorization": f"Bearer {bearer}"},
        json={
            "title": "Test TODO",
            "description": "Test TODO Description",
            "completed": False
        }
    )
    todo_id = response.json()["id"]

    # Delete the todo
    response = requests.delete(f"http://localhost:8000/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {bearer}"})
    assert response.status_code == 200

    # Try to get the deleted todo
    response = requests.get(f"http://localhost:8000/api/todos/{todo_id}",
        headers={"Authorization": f"Bearer {bearer}"})
    assert response.status_code == 404
