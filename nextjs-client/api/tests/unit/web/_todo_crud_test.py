import requests
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
from pathlib import Path

# Prep to import the app fastapi object and create a test client
current_dir = Path(__file__).resolve().parent

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))
from api.index import app


client = TestClient(app)


def get_bearer_token():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/login",
        data=login_data
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def bearer():
    return get_bearer_token()


@pytest.fixture(scope="module")
def mock_todo_id():
    todo_id = "1973c28c-7dc5-4a57-8a4c-b5db155621f2"
    return todo_id


@pytest.fixture(scope="module")
def invalid_todo_id():
    todo_id = "10c25fc2-835b-4ef3-bb3d-bf44fe496e"
    return todo_id

# GET /api/todps


def test_get_todos_unauthorized():
    response = client.get("/api/todos")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_todos(bearer):
    response = client.get(
        "/api/todos", headers={"Authorization": f"Bearer {bearer}"}
    )
    assert response.status_code == 200

# GET /api/todos/{todo_id}


def test_get_todo_by_id_unauthorized(mock_todo_id):
    response = client.get(f"/api/todos/{mock_todo_id}")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_todo_by_id_not_found(bearer, mock_todo_id):
    response = client.get(
        f"/api/todos/{mock_todo_id}", headers={"Authorization": f"Bearer {bearer}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

# DELETE /api/todos/{todo_id}


def test_delete_todo_invalid_id(bearer, invalid_todo_id):
    response = client.delete(
        f"/api/todos/{invalid_todo_id}", headers={"Authorization": f"Bearer {bearer}"}
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": [
                    "path",
                    "todo_id"
                ],
                "msg": "Input should be a valid UUID, invalid group length in group 4: expected 12, found 10",
                "input": "10c25fc2-835b-4ef3-bb3d-bf44fe496e",
                "ctx": {
                    "error": "invalid group length in group 4: expected 12, found 10"
                },
                "url": "https://errors.pydantic.dev/2.5/v/uuid_parsing"
            }
        ]
    }


def test_delete_todo_mock_id(bearer, mock_todo_id):
    response = client.delete(
        f"/api/todos/{mock_todo_id}", headers={"Authorization": f"Bearer {bearer}"}
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: Todo with id 1973c28c-7dc5-4a57-8a4c-b5db155621f2 not found"
    }

# PATCH /api/todos/{todo_id}

# Assert correct response structure and data
def test_update_invalid_todo_partial(bearer, invalid_todo_id):
    updated_todo = {"title": "Updated Title",
                    "description": "Updated Description"}
    response = client.patch(
        f"/api/todos/{invalid_todo_id}",
        headers={"Authorization": f"Bearer {bearer}"},
        json=updated_todo,
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": [
                    "path",
                    "todo_id"
                ],
                "msg": "Input should be a valid UUID, invalid group length in group 4: expected 12, found 10",
                "input": "10c25fc2-835b-4ef3-bb3d-bf44fe496e",
                "ctx": {
                    "error": "invalid group length in group 4: expected 12, found 10"
                },
                "url": "https://errors.pydantic.dev/2.5/v/uuid_parsing"
            }
        ]
    }


def test_update_todo_partial_authorized_notfound(bearer, mock_todo_id):
    updated_todo = {
        "title": "Coaster Cast"
    }
    response = client.patch(
        f"/api/todos/{mock_todo_id}",
        headers={"Authorization": f"Bearer {bearer}"},
        json=updated_todo,
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: 404: Todo not found"
    }

# Put /api/todos/{todo_id}
    
def test_update_invalid_todo_full(bearer, invalid_todo_id):
    updated_todo = {"title": "Updated Title",
                    "description": "Updated Description"}
    response = client.put(
        f"/api/todos/{invalid_todo_id}",
        headers={"Authorization": f"Bearer {bearer}"},
        json=updated_todo,
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": [
                    "path",
                    "todo_id"
                ],
                "msg": "Input should be a valid UUID, invalid group length in group 4: expected 12, found 10",
                "input": "10c25fc2-835b-4ef3-bb3d-bf44fe496e",
                "ctx": {
                    "error": "invalid group length in group 4: expected 12, found 10"
                },
                "url": "https://errors.pydantic.dev/2.5/v/uuid_parsing"
            }
        ]
    }

def test_update_todo_full_authorized_notfound(bearer, mock_todo_id):
    updated_todo = {
        "title": "Coaster Cast"
    }
    response = client.put(
        f"/api/todos/{mock_todo_id}",
        headers={"Authorization": f"Bearer {bearer}"},
        json=updated_todo,
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: 404: Todo not found"
    }

# POST /api/todos
    
def test_create_todo_unauthorized():
    response = client.post("/api/todos")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_todo_invalid(bearer):
    new_todo = {
        "title": "Coaster Cast"
    }
    response = client.post(
        "/api/todos",
        headers={"Authorization": f"Bearer {bearer + 'invalid'}"},
        json=new_todo,
    )

    assert response.status_code == 401
    assert response.json() == {
    "detail": "Invalid authentication credentials"
}
    
def test_create_todo_valid(bearer):
    new_todo = {
        "description": "cold"
    }
    response = client.post(
        "/api/todos",
        headers={"Authorization": f"Bearer {bearer}"},
        json=new_todo,
    )

    assert response.status_code == 422
    assert response.json() =={
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "title"
            ],
            "msg": "Field required",
            "input": {
                "description": "cold"
            },
            "url": "https://errors.pydantic.dev/2.5/v/missing"
        }
    ]
}