import pytest
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import sys
from pathlib import Path
# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

print("current_dir===========", current_dir)

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))

from api.service._user_auth import (authenticate_user, create_access_token, get_current_user, 
                                    service_login_for_access_token, service_signup_users, gpt_tokens_service)
from api.models._user_auth import RegisterUser

def test_authenticate_user(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_user = mocker.Mock()
    mock_user.hashed_password = "hashed_password"
    mocker.patch('api.service._user_auth.get_user', return_value=mock_user)
    mocker.patch('api.service._user_auth.verify_password', return_value=True)

    result = authenticate_user(mock_db, "username", "password")

    assert result == mock_user

def test_create_access_token(mocker):
    mocker.patch('api.service._user_auth.jwt.encode', return_value="encoded_jwt")

    result = create_access_token({"sub": "username", "id": "user_id"}, timedelta(minutes=30))

    assert result == "encoded_jwt"

def test_authenticate_user_nonexistent_user(mocker):
    mock_db = mocker.Mock(spec=Session)
    mocker.patch('api.service._user_auth.get_user', return_value=None)

    result = authenticate_user(mock_db, "nonexistent_username", "password")

    assert result == False

    
@pytest.mark.asyncio
async def test_get_current_user(mocker):
    mock_db = mocker.Mock(spec=Session)
    mocker.patch('api.service._user_auth.jwt.decode', return_value={"sub": "username"})
    mock_user = mocker.Mock()
    mocker.patch('api.service._user_auth.get_user', return_value=mock_user)

    result = await get_current_user("token", mock_db)

    assert result == mock_user

@pytest.mark.asyncio
async def test_service_login_for_access_token(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_form_data = mocker.Mock(spec=OAuth2PasswordRequestForm)
    mock_form_data.username = "username"
    mock_form_data.password = "password"
    mock_user = mocker.Mock()
    mock_user.username = "username"
    mock_user.id = "user_id"
    mocker.patch('api.service._user_auth.authenticate_user', return_value=mock_user)
    mocker.patch('api.service._user_auth.create_access_token', return_value="access_token")
    mocker.patch('api.service._user_auth.create_refresh_token', return_value="refresh_token")

    result = await service_login_for_access_token(mock_form_data, mock_db)

    assert result["access_token"] == "access_token"
    assert result["token_type"] == "bearer"
    assert result["user"] == mock_user
    assert result["refresh_token"] == "refresh_token"

@pytest.mark.asyncio
async def test_service_signup_users(mocker):
    mock_db = mocker.Mock(spec=Session)
    mock_user_data = mocker.Mock(spec=RegisterUser)
    mocker.patch('api.service._user_auth.db_signup_users', return_value="user")

    result = await service_signup_users(mock_user_data, mock_db)

    assert result == "user"

@pytest.mark.asyncio
async def test_gpt_tokens_service(mocker):
    mocker.patch('api.service._user_auth.validate_refresh_token', return_value="user_id")
    mocker.patch('api.service._user_auth.create_access_token', return_value="access_token")
    mocker.patch('api.service._user_auth.create_refresh_token', return_value="refresh_token")

    result = await gpt_tokens_service("refresh_token", "refresh_token")

    assert result["access_token"] == "access_token"
    assert result["token_type"] == "bearer"
    assert result["refresh_token"] == "refresh_token"

