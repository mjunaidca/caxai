import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from ....data.sqlalchemy_models import TODO
from ....models.todo_crud import TODOBase
from ....service import todos_crud


@pytest.fixture
def sample_todo():
    return TODO(id=UUID("12345678123456781234567812345678"), title="Test TODO", description="This is a test TODO")


def test_get_all_todo_data(sample_todo):
    mock_session = Mock(spec=Session)
    mock_session.query().all.return_value = [sample_todo]

    with patch('sqlalchemy.orm.Session', return_value=mock_session):
        result = todos_crud.get_all_todo_data(mock_session)

    assert result == [sample_todo]
    mock_session.query.assert_called_with(TODO)
    mock_session.query().all.assert_called_once()


