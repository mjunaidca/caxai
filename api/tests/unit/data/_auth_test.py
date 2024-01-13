import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

import sys
from pathlib import Path
# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

print("current_dir===========", current_dir)

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))

from api.models._user_auth import RegisterUser
from api.data._user_auth import get_user, db_signup_users, InvalidUserException

class TestUserAuthData:
    @pytest.fixture
    def setup(self):
        self.db = Mock(spec=Session)
        self.username = "testuser"
        self.user_data = RegisterUser(username="testuser", email="testuser@example.com", password="testpassword", full_name="Test User")

    def test_get_user_no_username(self, setup):
        with pytest.raises(InvalidUserException) as excinfo:
            get_user(self.db)
        assert str(excinfo.value) == "Username not provided"

    @pytest.mark.asyncio
    @patch('sqlalchemy.orm.Session.query')
    async def test_db_signup_users_existing_user(self, mock_query, setup):
        mock_query.return_value.filter.return_value.first.return_value = self.user_data
        with pytest.raises(InvalidUserException) as excinfo:
            await db_signup_users(self.user_data, self.db)
        assert str(excinfo.value) == "Email or username already registered"


    # @patch('sqlalchemy.orm.Session.query')
    # def test_get_user_not_found(self, mock_query, setup):
    #     mock_query.return_value.filter.return_value.first.return_value = None
    #     with pytest.raises(InvalidUserException) as excinfo:
    #         get_user(self.db, self.username)
    #     assert str(excinfo.value) == "User not found"

    # @patch('sqlalchemy.orm.Session.query')
    # def test_get_user_success(self, mock_query, setup):
    #     mock_query.return_value.filter.return_value.first.return_value = self.user_data
    #     result = get_user(self.db, self.username)
    #     assert result == self.user_data