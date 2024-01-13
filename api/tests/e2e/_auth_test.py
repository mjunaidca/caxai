
import requests
import pytest


@pytest.fixture
def temp_code():
    response = requests.get(
        "http://localhost:8000/api/oauth/temp-code?user_id=471db65c-6c9c-47d6-afc4-250dd4583baf"
    )
    data = response.json()
    code = data["code"]
    return code


@pytest.fixture
def refresh_token():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/login",
        data=login_data  # Send as form data
    )
    assert response.status_code == 200
    data = response.json()
    return data["refresh_token"]

# Test Authorization Endpoints

# LOGIN


def test_login_with_in_valid_credentials():
    login_data = {
        "username": "junaid",
        "password": "1jun45aid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/login",
        data=login_data  # Send as form data
    )
    # If you are expecting a 401 Unauthorized, then use 401 in the assertion
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_with_valid_credentials():
    login_data = {
        "username": "junaid",
        "password": "junaid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/login",
        data=login_data  # Send as form data
    )
    assert response.status_code == 200


# REGISTER
def test_register_with_already_registerd_email():
    register_data = {
        "username": "string",
        "email": "junaid@gmail.com",
        "full_name": "string",
        "password": "string"
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/signup",
        json=register_data
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email or username already registered"}


def test_register_with_already_registerd_username():
    register_data = {
        "username": "junaid",
        "email": "string@gmail.com",
        "full_name": "string",
        "password": "string"
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/oauth/signup",
        json=register_data
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email or username already registered"}

# OAUTH Code Flow Temp Code Endpoint


def test_get_oauth_temp_code():
    response = requests.get(
        "http://localhost:8000/api/oauth/temp-code?user_id=471db65c-6c9c-47d6-afc4-250dd4583baf"
    )
    assert response.status_code == 200

# OAUTH Code Flow Token Endpoints

    # Authorized Code Grant Type


def test_token_manager_valid(temp_code):
    print("temp_code", temp_code)
    response = requests.post(
        "http://localhost:8000/api/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": temp_code
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # check if access_token and refresh_token are in response
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

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

# OAUTH Code Flow Refresh Token Endpoint


def test_refresh_code_grant_valid(refresh_token):
    response = requests.post(
        "http://localhost:8000/api/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # check if access_token and refresh_token are in response
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

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

# test invalid temp code


def test_token_manager_invalid_tempcode():
    response = requests.post(
        "http://localhost:8000/api/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": "invalid_temp_code"
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}


def test_token_manager_invalid_refresh_token():
    response = requests.post(
        "http://localhost:8000/api/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": "invalid_refresh_token"
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": {
        "error": "invalid_token",
        "error_description": "The access token expired"
    }
    }

# Missing Grant


def test_token_manager_missing_grant():
    response = requests.post(
        "http://localhost:8000/api/oauth/token",
        data={
            "code": "invalid_temp_code"
        }
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "grant_type"
                ],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }
