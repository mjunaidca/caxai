from fastapi import APIRouter, HTTPException, Depends
from ..data.db_config import get_db
from ..data.sqlalchemy_models import TODO
from sqlalchemy.orm import Session
from ..models.todo import TODOBase
from uuid import uuid1
from datetime import datetime

router = APIRouter(prefix="/api")


@router.post("/todos/", response_model=TODOBase)
def create_todo(todo: TODOBase, db: Session = Depends(get_db)):
    """
    Create a new TODO item.

    Args:
        todo (TODOBase): The TODO item to be created. Pydantic Model Validation
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        TODOCreate: The created TODO item.
    """

    db_todo = TODO(id=uuid1(), title=todo.title,description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# @router.put("/todos/{todo_id}", response_model=TodoDBSchema)
# def update_todo(todo_id: int, updated_todo: TodoCreateSchema, db: Session = Depends(get_db)):
#     db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if db_todo is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     update_data = updated_todo.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_todo, key, value)
#     db.commit()
#     return db_todo


# @router.get("/todos/", response_model=list[TodoDBSchema])
# def get_todos(db: Session = Depends(get_db)):
#     db_todo = db.query(Todo)
#     return db_todo


# @router.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int, db: Session = Depends(get_db)):
#     db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
#     if db_todo is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     db.delete(db_todo)
#     db.commit()
#     return {"message": "Todo deleted"}
