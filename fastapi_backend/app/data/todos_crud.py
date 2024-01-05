from ..data.sqlalchemy_models import TODO
from sqlalchemy.orm import Session
from uuid import uuid1
from sqlalchemy.exc import SQLAlchemyError

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