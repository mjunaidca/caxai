from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Query, Body, Form
from fastapi.security import OAuth2PasswordRequestForm

from uuid import UUID
from datetime import timedelta

from .data._db_config import get_db
from .models._user_auth import RegisterUser, UserOutput, LoginResonse, Token
from .service._user_auth import service_signup_users, service_login_for_access_token, create_access_token
from .data._db_config import get_db
from .models._todo_crud import TODOBase, TODOResponse, PaginatedTodos
from .service._todos_crud import create_todo_service, get_todo_by_id_service, get_all_todos_service, full_update_todo_service, partial_update_todo_service, delete_todo_data
from .utils._helpers import get_current_user_dep

app = FastAPI(
    title="Cal AI",
    description="A multi-user to-do application for efficient task management.",
    version="1.0.0",
    terms_of_service="https://todo-auth-two.vercel.app/terms/",
    contact={
        "name": "Muhammad Junaid",
        "url": "hhttps://todo-auth-two.vercel.app/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    servers=[
        {
            "url": "https://todo-auth-two.vercel.app",
            "description": "Production server"
        },
    ]
)

# Hello World
@app.get("/api", tags=["Welcome"])
def read_root():
    return {"Hello": "World"}

# user_auth.py web layer routes
@app.post("/api/auth/login", response_model=LoginResonse, tags=["Authentication"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return await service_login_for_access_token(form_data, db)

# Get Access Token against user_id
@app.post("/api/token", response_model=Token, tags=["Authentication"])
async def get_access_token(code: Annotated[UUID, Form()]):
    access_token_expires = timedelta(minutes=float(120))
    access_token = create_access_token(data={"id": code}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/api/auth/signup", response_model=UserOutput, tags=["Authentication"])
async def signup_users(
    user_data: RegisterUser, db: Session = Depends(get_db)
):
    return await service_signup_users(user_data, db)

#  todos_crud.py web layer routes

# Get ALL TODOS
@app.get("/api/todos", response_model=PaginatedTodos, tags=["TODO Crud"])
def get_todos(db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep), page: int = Query(1, description="Page number", ge=1),
              per_page: int = Query(10, description="Items per page", ge=1, le=100)):
    try:
        # Calculate the offset to skip the appropriate number of items
        offset = (page - 1) * per_page
        all_todos = get_all_todos_service(db, user_id, offset, per_page)

        # Calculate next and previous page URLs
        next_page = f"?page={page + 1}&per_page={per_page}" if len(all_todos) == per_page else None
        previous_page = f"?page={page - 1}&per_page={per_page}" if page > 1 else None

        # Return data in paginated format
        paginated_data = {"count": len(all_todos), "next": next_page, "previous": previous_page, "todos": all_todos}

        return paginated_data
        # return get_all_todos_service(db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Get a Single TODO item


@app.get("/api/todos/{todo_id}", response_model=TODOResponse, tags=["TODO Crud"])
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
@app.post("/api/todos", response_model=TODOResponse, tags=["TODO Crud"])
def create_todo(todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return create_todo_service(todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Update a Single TODO item Completly


@app.put("/api/todos/{todo_id}", response_model=TODOResponse, tags=["TODO Crud"])
def update_todo(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return full_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Update a Single TODO item partially
@app.patch("/api/todos/{todo_id}", response_model=TODOResponse, tags=["TODO Crud"])
def update_todo_partial(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return partial_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# DELETE a single TODO item
@app.delete("/api/todos/{todo_id}", tags=["TODO Crud"])
def delete_todo(todo_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    try:
        return delete_todo_data(todo_id, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
