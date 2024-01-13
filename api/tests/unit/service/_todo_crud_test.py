import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from sqlalchemy.orm import Session

import sys
from pathlib import Path
# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

print("current_dir===========", current_dir)

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))

from api.models._todo_crud import TODOBase, TODOResponse
from api.data._todos_crud import TodoNotFoundError
from api.service._todos_crud import get_all_todos_service, get_todo_by_id_service, create_todo_service, full_update_todo_service, partial_update_todo_service, delete_todo_service


class TestTodoService:
    """
    This allows the tests to check that the service functions call the data functions correctly 
    without actually interacting with the database. The Mock class is used to create a mock database 
    session, and the uuid4 function is used to create mock UUIDs. The TODOBase class is used to 
    create a mock TODO item.
    """
    @pytest.fixture
    def setup(self):
        self.db = Mock(spec=Session)
        self.user_id = uuid4()
        self.todo_id = uuid4()
        self.todo_data = TODOBase(title="Test", description="Test description", completed=False)

    @patch('api.service._todos_crud.get_all_todo_data')
    def test_get_all_todos_service(self, mock_get_all, setup):
        get_all_todos_service(self.db, self.user_id, 0, 10)
        mock_get_all.assert_called_once_with(self.db, self.user_id, 0, 10)

    @patch('api.service._todos_crud.get_single_todo_data')
    def test_get_todo_by_id_service(self, mock_get_single, setup):
        get_todo_by_id_service(self.todo_id, self.db, self.user_id)
        mock_get_single.assert_called_once_with(self.todo_id, self.db, self.user_id)

    @patch('api.service._todos_crud.create_todo_data')
    def test_create_todo_service(self, mock_create, setup):
        create_todo_service(self.todo_data, self.db, self.user_id)
        mock_create.assert_called_once()

    @patch('api.service._todos_crud.full_update_todo_data')
    def test_full_update_todo_service(self, mock_update, setup):
        full_update_todo_service(self.todo_id, self.todo_data, self.db, self.user_id)
        mock_update.assert_called_once_with(self.todo_id, self.todo_data, self.db, self.user_id)

    @patch('api.service._todos_crud.partial_update_todo_data')
    def test_partial_update_todo_service(self, mock_update, setup):
        partial_update_todo_service(self.todo_id, self.todo_data, self.db, self.user_id)
        mock_update.assert_called_once_with(self.todo_id, self.todo_data, self.db, self.user_id)

    @patch('api.service._todos_crud.delete_todo_data')
    def test_delete_todo_service(self, mock_delete, setup):
        delete_todo_service(self.todo_id, self.db, self.user_id)
        mock_delete.assert_called_once_with(self.todo_id, self.db, self.user_id)


    
