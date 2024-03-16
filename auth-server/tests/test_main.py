from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException

from uuid import UUID
import pytest
from unittest.mock import patch, AsyncMock
from sqlmodel import SQLModel, create_engine, Session

# Now you can use relative imports
from app.main import app
from app.core import settings
from app.core.config_db import get_db
from app.core.utils import get_password_hash
from app.models import LoginResonse, UserOutput, UserInDB, RegisterUser, UserInDB, UserOutput


connection_string = str(settings.TEST_DB_URL).replace(
"postgresql", "postgresql+psycopg")

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

SQLModel.metadata.create_all(engine)


def get_session_override():
    with Session(engine) as session:
        return session

app.dependency_overrides[get_db] = get_session_override
client = TestClient(app=app)



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

# /api/oauth/token
@pytest.fixture
def mock_create_access_token():
    expected_code = "testcode"
    with patch('app.main.create_access_token', return_value=expected_code):
        yield expected_code


# Endpoints for OAuth2 Authentication

# api/oauth/signup
def test_signup_missing_fullname(): 
    response = client.post("/api/oauth/signup", json={"email": "test1@example.com", "username": "test1"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'full_name'], 'msg': 'Field required', 'input': {'email': 'test1@example.com', 'username': 'test1'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}, {'type': 'missing', 'loc': ['body', 'password'], 'msg': 'Field required', 'input': {'email': 'test1@example.com', 'username': 'test1'}, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}



# Test login with incomplete data: Send incomplete form data and assert validation errors.
def test_login_with_incomplete_data():
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

    with patch('app.main.create_access_token', return_value=expected_code):
        response = client.get(f"/api/oauth/temp-code?user_id={user_id}")

        assert response.status_code == 200
        response_data = response.json()

        assert 'code' in response_data
        assert response_data['code'] == expected_code



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



def test_tokens_manager_oauth_code_flow_with_failed_refresh_token():

    # Mock gpt_tokens_service to raise an HTTPException for an invalid or expired token
    with patch('app.service.gpt_tokens_service') as mock_service:
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
    with patch('app.service.validate_refresh_token', new_callable=AsyncMock, return_value="some_user_id"):
        # Mock gpt_tokens_service to return the mock response
        with patch('app.service.gpt_tokens_service', return_value=mock_response):
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