from ..data.sqlalchemy_models import TODO
from sqlalchemy.orm import Session
from ..models.todo_crud import TODOBase
from ..data.todos_crud import create_todo_data


def create_todo_service(todo_data: TODOBase, db: Session) -> TODO:
    """
    Create a new TODO item.

    Args:
        todo_data (TODOBase): The TODO item to be created. Pydantic Model Validation
        db (Session): The database session.

    Returns:
        TODO: The created TODO item.
    """
    try:
        db_todo = TODO(title=todo_data.title, description=todo_data.description, completed=todo_data.completed)
        return create_todo_data(db_todo, db)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error creating TODO item: {e}")
        # Re-raise the exception to be handled at the endpoint level
        raise