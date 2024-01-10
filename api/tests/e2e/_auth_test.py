
import requests

# Test Authorization Endpoints

# LOGIN


def test_login_with_in_valid_credentials():
    login_data = {
        "username": "junaid",
        "password": "1jun45aid"
    }
    response = requests.post(
        "http://127.0.0.1:8000/api/auth/login",
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
        "http://127.0.0.1:8000/api/auth/login",
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
        "http://127.0.0.1:8000/api/auth/signup",
        json=register_data
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email or username already registered"}

def test_register_with_already_registerd_username():
    register_data = {
        "username": "junaid",
        "email": "string@gmail.com",
        "full_name": "string",
        "password": "string"
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/auth/signup",
        json=register_data
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email or username already registered"}
