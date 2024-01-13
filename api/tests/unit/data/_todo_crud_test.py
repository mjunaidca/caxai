import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

import sys
from pathlib import Path
# Determine the directory of the current file (env.py)
current_dir = Path(__file__).resolve().parent

print("current_dir===========", current_dir)

# Add the grand grandparent directory ... (the root of your FastAPI application) to sys.path
sys.path.append(str(current_dir.parent.parent.parent.parent))

from api.data._todos_crud import get_all_todo_data, get_single_todo_data, create_todo_data, full_update_todo_data, partial_update_todo_data, delete_todo_data, TodoNotFoundError
from api.data._sqlalchemy_models import TODO
from api.models._todo_crud import TODOBase

def test_get_all_todo_data():
    db = Mock()
    user_id = uuid4()
    offset = 0
    per_page = 10

    with patch('api.data._todos_crud.TODO') as mock_todo:
        get_all_todo_data(db, user_id, offset, per_page)
        db.query.assert_called_once_with(mock_todo)
        db.query().filter.assert_called_once_with(mock_todo.user_id == user_id)
        db.query().filter().offset.assert_called_once_with(offset)
        db.query().filter().offset().limit.assert_called_once_with(per_page)
        db.query().filter().offset().limit().all.assert_called_once()

def test_get_single_todo_data():
    db = Mock()
    todo_id = uuid4()
    user_id = uuid4()

    with patch('api.data._todos_crud.TODO') as mock_todo:
        get_single_todo_data(todo_id, db, user_id)
        db.query.assert_called_once_with(mock_todo)
        db.query().filter.assert_called_once_with(mock_todo.id == todo_id, mock_todo.user_id == user_id)
        db.query().filter().first.assert_called_once()

def test_create_todo_data():
    db = Mock()
    db_todo = Mock()

    create_todo_data(db_todo, db)
    db.add.assert_called_once_with(db_todo)
    db.commit.assert_called_once()

def test_full_update_todo_data():
    db = Mock()
    todo_id = uuid4()
    todo_data = TODOBase(title="Test", description="Test description")
    user_id = uuid4()

    with patch('api.data._todos_crud.TODO') as mock_todo:
        full_update_todo_data(todo_id, todo_data, db, user_id)
        db.query.assert_called_once_with(mock_todo)
        db.query().filter.assert_called_once_with(mock_todo.id == todo_id, mock_todo.user_id == user_id)
        db.query().filter().first.assert_called_once()
        db.commit.assert_called_once()

def test_partial_update_todo_data():
    db = Mock()
    todo_id = uuid4()
    todo_data = TODOBase(title="Test", description="Test description")
    user_id = uuid4()

    with patch('api.data._todos_crud.TODO') as mock_todo:
        partial_update_todo_data(todo_id, todo_data, db, user_id)
        db.query.assert_called_once_with(mock_todo)
        db.query().filter.assert_called_once_with(mock_todo.id == todo_id, mock_todo.user_id == user_id)
        db.query().filter().first.assert_called_once()
        db.commit.assert_called_once()

def test_delete_todo_data():
    db = Mock()
    todo_id = uuid4()
    user_id = uuid4()

    with patch('api.data._todos_crud.TODO') as mock_todo:
        delete_todo_data(todo_id, db, user_id)
        db.query.assert_called_once_with(mock_todo)
        db.query().filter.assert_called_once_with(mock_todo.id == todo_id, mock_todo.user_id == user_id)
        db.query().filter().first.assert_called_once()
        db.delete.assert_called_once()
        db.commit.assert_called_once()