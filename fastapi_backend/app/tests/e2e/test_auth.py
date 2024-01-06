
import requests

def test_login_with_in_valid_credentials():
    login_data = {
        "username": "mjs",
        "password": "mjss"
    }
    response = requests.post(
        "http://localhost:8000/api/auth/login",
        data=login_data  # Send as form data
    )
    # If you are expecting a 401 Unauthorized, then use 401 in the assertion
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
