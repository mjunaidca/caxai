"""
Unit Tests for TODO CRUD Routes
"""

import requests
import pytest
from unittest.mock import patch, MagicMock, AsyncMock, ANY
from uuid import UUID
from fastapi.testclient import TestClient

import sys
from pathlib import Path

# Prep to import the app fastapi object and create a test client
current_dir = Path(__file__).resolve().parent

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent))

# Now you can use relative imports
from api.models._user_auth import LoginResonse, UserOutput, UserInDB, RegisterUser
from api.utils._helpers import get_password_hash
from api.index import app


@pytest.fixture
def client():
    return TestClient(app)

# Create Resuable Pytest Fixtures


@pytest.fixture
def mock_user_db():
    test_password = "testpass"
    hashed_password = get_password_hash(test_password)
    return UserInDB(
        id=UUID("123e4567-e89b-12d3-a456-426655440000"),
        username="test",
        hashed_password=hashed_password,
        email="test@example.com",
        full_name="Test User",
        email_verified=True
    )


@pytest.fixture
def mock_user_output(mock_user_db):
    return UserOutput(
        id=mock_user_db.id,
        username=mock_user_db.username,
        email=mock_user_db.email,
        full_name=mock_user_db.full_name,
        email_verified=mock_user_db.email_verified
    )


@pytest.fixture
def mock_login_response(mock_user_output):
    return LoginResonse(
        access_token='testtoken',
        token_type='bearer',
        user=mock_user_output
    )


# /api/auth/login
# Test successful login: Send valid credentials and assert the correct response.
def test_successful_login(client, mock_user_db, mock_user_output, mock_login_response):
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock) as mock_login_service, \
            patch('api.service._user_auth.get_user', return_value=mock_user_db):
        response = client.post(
            "/api/auth/login", data={"username": "test", "password": "testpass"})

        assert response.status_code == 200
        response_data = response.json()

        assert 'access_token' in response_data
        assert isinstance(response_data['access_token'], str)
        assert response_data['access_token']
        assert response_data['token_type'] == 'bearer'
        assert response_data['user'] == {
            'id': str(mock_user_output.id),
            'username': mock_user_output.username,
            'email': mock_user_output.email,
            'full_name': mock_user_output.full_name,
            'email_verified': mock_user_output.email_verified
        }

        # TODO: mock_login_service.assert_called_once()

# Test login with invalid credentials: Send invalid credentials and assert the appropriate error response.


def test_login_with_invalid_credentials(client):
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock) as mock_login_service, \
            patch('api.service._user_auth.get_user', return_value=None):
        response = client.post(
            "/api/auth/login", data={"username": "wrong_user", "password": "wrong_password"})

        assert response.status_code == 401
        response_data = response.json()

        assert 'detail' in response_data
        assert response_data['detail'] == 'Incorrect username or password'

# Test login with incomplete data: Send incomplete form data and assert validation errors.


def test_login_with_incomplete_data(client):
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock) as mock_login_service, \
            patch('api.service._user_auth.get_user', return_value=None):
        response = client.post("/api/auth/login", data={"username": "test"})

        assert response.status_code == 422
        response_data = response.json()

        assert 'detail' in response_data
        assert isinstance(response_data['detail'], list)
        assert len(response_data['detail']) > 0
        assert response_data['detail'][0]['loc'] == ['body', 'password']
        assert response_data['detail'][0]['msg'] == 'Field required'
        assert response_data['detail'][0]['type'] == 'missing'

# TODO: /api/auth/signup
# Test successful signup: Send valid user data and assert the correct response.
# Test signup with existing user: Send data for an existing user and assert the appropriate error response.
# Test signup with invalid data: Send invalid user data and assert validation errors.


def get_bearer_token():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/auth/login",
        data=login_data
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def bearer():
    return get_bearer_token()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_retrieve_all_todos(client, bearer):
    base_url = "http://127.0.0.1:8000/api/todos"
    headers = {"Authorization": f"Bearer {bearer}"}
    response = client.get(base_url, headers=headers)
    assert response.status_code == 200
    # Assert correct response structure and data

# TODO: Add remaining tests for the todo crud web layer