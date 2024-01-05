from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from uuid import UUID

from ..data.db_config import get_db
from ..models.todo_crud import TODOBase, TODOResponse
from ..service.todos_crud import create_todo_service

from ..data.sqlalchemy_models import TODO

router = APIRouter(prefix="/api")

# Get ALL TODOS
@router.get("/todos/", response_model=list[TODOResponse])
def get_todos(db: Session = Depends(get_db)):
    db_todo = db.query(TODO)
    return db_todo

# Get a Single TODO item
@router.get("/todos/{todo_id}", response_model=TODOResponse)
def get_todo_by_id(todo_id: UUID, db: Session = Depends(get_db)):
    db_todo = db.query(TODO).filter(TODO.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# Create a new TODO item
@router.post("/todos/", response_model=TODOResponse)
def create_todo(todo: TODOBase, db: Session = Depends(get_db)):
    try:
        return create_todo_service(todo, db)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Update a Single TODO item Completly
@router.put("/todos/{todo_id}", response_model=TODOResponse)
def update_todo(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db)):
    db_todo = db.query(TODO).filter(TODO.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    update_data = updated_todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo

# Update a Single TODO item partially
@router.patch("/todos/{todo_id}", response_model=TODOResponse)
def update_todo_partial(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db)):
    db_todo = db.query(TODO).filter(TODO.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    update_data = updated_todo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo


# DELETE a single TODO item
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    db_todo = db.query(TODO).filter(TODO.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}
