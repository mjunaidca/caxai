from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from uuid import UUID

from ..data.db_config import get_db
from ..models.todo_crud import TODOBase, TODOResponse
from ..service.todos_crud import create_todo_service, get_todo_by_id_service, get_all_todos_service, full_update_todo_service, partial_update_todo_service, delete_todo_data
from ..utils.helpers import get_current_user_dep

router = APIRouter(prefix="/api/todos", tags=["Todo Crud"])
# We are not adding this at router level as we need user_id in each operand, else it will run twice: dependencies=[Depends(get_current_user_dep)] 

# Get ALL TODOS
@router.get("/", response_model=list[TODOResponse])
def get_todos(db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return get_all_todos_service(db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Get a Single TODO item
@router.get("/{todo_id}", response_model=TODOResponse)
def get_todo_by_id(todo_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return get_todo_by_id_service(todo_id, db, user_id)
    except HTTPException as e:
        # If the service layer raised an HTTPException, re-raise it
        raise e
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Create a new TODO item
@router.post("/", response_model=TODOResponse)
def create_todo(todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return create_todo_service(todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Update a Single TODO item Completly


@router.put("/{todo_id}", response_model=TODOResponse)
def update_todo(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return full_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Update a Single TODO item partially
@router.patch("/{todo_id}", response_model=TODOResponse)
def update_todo_partial(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return partial_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# DELETE a single TODO item
@router.delete("/{todo_id}")
def delete_todo(todo_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return delete_todo_data(todo_id, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
