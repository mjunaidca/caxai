from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..data._sqlalchemy_models import TODO
from ..models._todo_crud import TODOBase, TODOResponse
from ..data._todos_crud import create_todo_data, get_single_todo_data, get_all_todo_data, full_update_todo_data, partial_update_todo_data, delete_todo_data, TodoNotFoundError

from uuid import UUID

# get all TODO items
def get_all_todos_service(db: Session, user_id: UUID, offset: int, per_page: int) -> list[TODOResponse]:
    """
    Get all TODO items with pagination from the database.

    Args:
        db (Session): The database session.
        user_id (UUID): The user's ID.
        offset (int): The number of items to skip.
        per_page (int): The number of items per page.

    Returns:
        List[TODO]: The list of TODO items.
    """
    try:
        get_todos: list[TODO] = get_all_todo_data(db, user_id, offset, per_page)
        return [TODOResponse.model_validate(todo) for todo in get_todos]
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error getting all TODO items with pagination: {e}")
        # Re-raise the exception to be handled at the endpoint level
        raise

# get a single TODO item
def get_todo_by_id_service(todo_id: UUID, db: Session, user_id: UUID) -> TODO:
    try:
        todo = get_single_todo_data(todo_id, db, user_id)
        return todo
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")
    except SQLAlchemyError as e:
        # Handle database errors
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error getting TODO item: {e}")
        # Re-raise the exception to be handled at the endpoint level
        raise HTTPException(status_code=500, detail="Internal server error")


def create_todo_service(todo_data: TODOBase, db: Session, user_id: UUID) -> TODO:
    """
    Create a new TODO item.

    Args:
        todo (TODOSchema): The TODO item to be created.
        db (Session): The database session.

    Raises:
        HTTPException: If there is a database error or an unexpected error.

    Returns:
        TODO: The created TODO item.
    """
    try:
        db_todo = TODO(title=todo_data.title,
                       description=todo_data.description, completed=todo_data.completed, user_id=user_id)
        return create_todo_data(db_todo, db)
    except SQLAlchemyError as e:
        print(f"Database error when creating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"Error creating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def full_update_todo_service(todo_id: UUID, todo_data: TODOBase, db: Session, user_id: UUID) -> TODO:
    """
    Update an existing TODO item.

    Args:
        todo_id (UUID): The ID of the TODO item to be updated.
        todo (TODOSchema): The updated TODO item.
        db (Session): The database session.

    Raises:
        HTTPException: If the TODO item is not found, or if there is a database error or an unexpected error.

    Returns:
        TODO: The updated TODO item.
    """
    try:
        return full_update_todo_data(todo_id, todo_data, db, user_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")
    except SQLAlchemyError as e:
        print(f"Database error when updating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"Error updating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def partial_update_todo_service(todo_id: UUID, todo_data: TODOBase, db: Session, user_id: UUID) -> TODO:
    """
    Partially update an existing TODO item.

    Args:
        todo_id (str): The ID of the TODO item to update.
        todo_data (TODOBase): The updated TODO item data.
        db (Session): The database session.

    Returns:
        TODO: The updated TODO item.
    """
    try:
        return partial_update_todo_data(todo_id, todo_data, db, user_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")
    except SQLAlchemyError as e:
        print(f"Database error when updating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"Error updating TODO item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def delete_todo_service(todo_id: UUID, db: Session, user_id: UUID) -> None:
    """
    Delete a TODO item from the database.

    Args:
        todo_id (str): The ID of the TODO item to delete.
        db (Session): The database session.
    """
    try:
        return delete_todo_data(todo_id, db, user_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")
    except SQLAlchemyError as e:
        print(f"Database error when deleting TODO item: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"Error deleting TODO item: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
