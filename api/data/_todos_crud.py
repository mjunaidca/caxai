from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

from ._sqlalchemy_models import TODO
from ..models._todo_crud import TODOBase

class TodoNotFoundError(Exception):
    """
    Exception raised when a TODO item is not found in the database.
    """
    pass

# get all TODO items
# get all TODO items
def get_all_todo_data(db: Session, user_id: UUID, offset: int, per_page: int) -> list[TODO]:
    """
    Get TODO items with pagination from the database.

    Args:
        db (Session): The database session.
        user_id (UUID): The user's ID.
        offset (int): The number of items to skip.
        per_page (int): The number of items per page.

    Returns:
        List[TODO]: The list of TODO items.
    """
    try:
        return db.query(TODO).filter(TODO.user_id == user_id).offset(offset).limit(per_page).all()
    except SQLAlchemyError as e:
        # Log the exception for debugging purposes
        print(f"Error getting TODO items with pagination: {e}")
        # Re-raise the exception to be handled at the endpoint level
        raise

# get a single TODO item
def get_single_todo_data(todo_id: UUID, db: Session, user_id: UUID) -> TODO:
    """
    Get a single TODO item from the database.

    Args:
        todo_id (str): The ID of the TODO item to retrieve.
        db (Session): The database session.

    Returns:
        TODO: The retrieved TODO item.
    """
    try:
        db_todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == user_id).first()
        if db_todo is None:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        return db_todo
    except SQLAlchemyError as e:
        # Log the exception for debugging purposes
        print(f"Error getting TODO item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise
    
def create_todo_data(db_todo: TODO, db: Session) -> TODO:
    """
    Create a new TODO item in the database.

    Args:
        db_todo (TODO): The TODO item to be created.
        db (Session): The database session.

    Returns:
        TODO: The created TODO item.
    """
    try:
        db.add(db_todo)
        db.commit()
        # db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"Error creating TODO item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise


def full_update_todo_data(todo_id: UUID, todo_data: TODOBase, db: Session, user_id: UUID) -> TODO:
    """
    Update an existing TODO item in the database.

    Args:
        todo_id (str): The ID of the TODO item to update.
        db_todo (TODO): The updated TODO item data.
        db (Session): The database session.

    Returns:
        TODO: The updated TODO item.
    """
    try:
        db_todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == user_id).first()
        if db_todo is None:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        update_data = todo_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        return db_todo
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"Error updating TODO item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise

def partial_update_todo_data(todo_id: UUID, todo_data: TODOBase, db: Session, user_id: UUID) -> TODO:
    try:
        db_todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == user_id).first()
        if db_todo is None:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        update_data = todo_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        return db_todo
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"Error updating TODO item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise

def delete_todo_data(todo_id: UUID, db: Session, user_id: UUID) -> None:
    """
    Delete an existing TODO item from the database.

    Args:
        todo_id (str): The ID of the TODO item to delete.
        db (Session): The database session.
    """
    try:
        db_todo = db.query(TODO).filter(TODO.id == todo_id, TODO.user_id == user_id).first()
        if db_todo is None:
            raise TodoNotFoundError(f"Todo with id {todo_id} not found")
        db.delete(db_todo)
        db.commit()
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"Error deleting TODO item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise