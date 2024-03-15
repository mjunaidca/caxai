from fastapi.testclient import TestClient
from pathlib import Path
import sys
from uuid import UUID
import pytest
from unittest.mock import patch, AsyncMock

# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

print("current_dir===========", current_dir)

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))

# Now you can use relative imports
from api.index import app
from api.utils._helpers import get_password_hash
from api.models._user_auth import LoginResonse, UserOutput, UserInDB, RegisterUser
from api.models._user_auth import UserInDB, UserOutput
from unittest.mock import patch
import pytest
from unittest.mock import patch
from uuid import UUID

client = TestClient(app)


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

# Endpoints for OAuth2 Authentication

# api/oauth/signup
def test_signup_missing_fullname(): 
    response = client.post("/api/oauth/signup", json={"email": "test@example.com", "username": "test"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "Field required",
                "input": {
                    "username": "test",
                    "email": "test@example.com"
                },
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }

@patch("api.service._user_auth.service_signup_users")
def test_signup_duplicate(mock_register_user):
    mock_register_user.side_effect = ValueError("Email or username already registered")

    response = client.post("/api/oauth/signup", json={ "email": "test@example.com", "username": "test", "password": "testpass"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email or username already registered"
    }



# /api/auth/login
# Test successful login: Send valid credentials and assert the correct response.
def test_successful_login(mock_user_db, mock_user_output):
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock), \
            patch('api.service._user_auth.get_user', return_value=mock_user_db):
        response = client.post(
            "/api/oauth/login", data={"username": "test", "password": "testpass"})

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

        # check if access_token and refresh_token are not empty
        assert response.json()["access_token"] != ""
        assert response.json()["refresh_token"] != ""

        # check if access_token and refresh_token are not None
        assert response.json()["access_token"] is not None
        assert response.json()["refresh_token"] is not None

        # check if access_token and refresh_token are not equal
        assert response.json()["access_token"] != response.json()["refresh_token"]

        # test expiry time and token type
        assert response.json()["expires_in"] is not None
        assert response.json()["token_type"] == "bearer"

# Test login with invalid credentials: Send invalid credentials and assert the appropriate error response.
def test_login_with_invalid_credentials():
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock) as mock_login_service, \
            patch('api.service._user_auth.get_user', return_value=None):
        response = client.post(
            "/api/oauth/login", data={"username": "wrong_user", "password": "wrong_password"})

        assert response.status_code == 401
        response_data = response.json()

        assert 'detail' in response_data
        assert response_data['detail'] == 'Incorrect username or password'

# Test login with incomplete data: Send incomplete form data and assert validation errors.
def test_login_with_incomplete_data():
    with patch('api.service._user_auth.service_login_for_access_token', new_callable=AsyncMock) as mock_login_service, \
            patch('api.service._user_auth.get_user', return_value=None):
        response = client.post("/api/oauth/login", data={"username": "test"})

        assert response.status_code == 422
        response_data = response.json()

        assert 'detail' in response_data
        assert isinstance(response_data['detail'], list)
        assert len(response_data['detail']) > 0
        assert response_data['detail'][0]['loc'] == ['body', 'password']
        assert response_data['detail'][0]['msg'] == 'Field required'
        assert response_data['detail'][0]['type'] == 'missing'

# /api/oauth/token
def test_get_temp_code():
    user_id = UUID("123e4567-e89b-12d3-a456-426655440000")
    expected_code = "testcode"

    with patch('api.index.create_access_token', return_value=expected_code):
        response = client.get(f"/api/oauth/temp-code?user_id={user_id}")

        assert response.status_code == 200
        response_data = response.json()

        assert 'code' in response_data
        assert response_data['code'] == expected_code


# /api/oauth/token
@pytest.fixture
def mock_create_access_token():
    expected_code = "testcode"
    with patch('api.index.create_access_token', return_value=expected_code):
        yield expected_code


def test_get_temp_code_fixture(mock_create_access_token):
    user_id = UUID("123e4567-e89b-12d3-a456-426655440000")
    expected_code = mock_create_access_token

    response = client.get(f"/api/oauth/temp-code?user_id={user_id}")

    assert response.status_code == 200
    response_data = response.json()

    assert 'code' in response_data
    assert response_data['code'] == expected_code


def test_tokens_manager_oauth_codeflow_missing_grant_type():
    response = client.post(
        "/api/oauth/token",
        data={
            "code": "testcode"
        }
    )

    assert response.status_code == 422
    response_data = response.json()

    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0
    assert response_data["detail"][0]["loc"] == ["body", "grant_type"]
    assert response_data["detail"][0]["msg"] == "Field required"
    assert response_data["detail"][0]["type"] == "missing"

from fastapi.exceptions import HTTPException


def test_tokens_manager_oauth_code_flow_with_failed_refresh_token():

    # Mock gpt_tokens_service to raise an HTTPException for an invalid or expired token
    with patch('api.service._user_auth.gpt_tokens_service') as mock_service:
        mock_service.side_effect = HTTPException(status_code=401, detail="Token invalid or expired")

        response = client.post(
            "/api/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": "testcode"
            }
        )

        # Assert that the response status code is 401 (Unauthorized)
        assert response.status_code == 401
        response_data = response.json()

        # Assert the error message is in the response
        assert "detail" in response_data
        assert response_data["detail"] == {'error': 'invalid_token', 'error_description': 'The access token expired'}


def test_tokens_manager_oauth_code_flow_with_refresh_token():

    # Mock data to be returned by gpt_tokens_service
    mock_response = {
        "access_token": "new_access_token",
        "token_type": "bearer",
        "expires_in": 3600,  # or any suitable expiry time
        "refresh_token": "new_refresh_token"
    }

    # Mock the validate_refresh_token function to return a user ID, simulating a valid refresh token
    with patch('api.service._user_auth.validate_refresh_token', new_callable=AsyncMock, return_value="some_user_id"):
        # Mock gpt_tokens_service to return the mock response
        with patch('api.service._user_auth.gpt_tokens_service', return_value=mock_response):
            response = client.post(
                "/api/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": "any_refresh_token"  # This token is assumed valid in the test context
                }
            )

            # Assert that the response status code is 200 (OK)
            assert response.status_code == 200
            response_data = response.json()

            # Assert that an access token is present and is a string
            assert "access_token" in response_data
            assert isinstance(response_data["access_token"], str)