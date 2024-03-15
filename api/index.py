from typing import Annotated, Optional
from sqlmodel import Session

from fastapi import Depends, FastAPI, HTTPException, Query, Form
from fastapi.security import OAuth2PasswordRequestForm

from uuid import UUID

# Now you can use relative imports
from .data._db_config import get_db
from .models._user_auth import RegisterUser, UserOutput, LoginResonse, GPTToken
from .models._todo_crud import TODOBase, TODOResponse, PaginatedTodos
from .service._user_auth import service_signup_users, service_login_for_access_token, create_access_token, gpt_tokens_service
from .service._todos_crud import create_todo_service, get_todo_by_id_service, get_all_todos_service, full_update_todo_service, partial_update_todo_service, delete_todo_data
from .utils._helpers import get_current_user_dep

app = FastAPI(
    title="Cax",
    description="A multi-user to-do microservice with NextJS14 web app and Multi User Custom GPT for efficient task management.",
    version="1.0.0",
    terms_of_service="https://caxgpt.vercel.app/terms/",
    contact={
        "name": "Muhammad Junaid",
        "url": "https://caxgpt.vercel.app/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    servers=[
        {
            "url": "https://caxgpt.vercel.app",
            "description": "Production server"
        },
    ],
    docs_url="/api/docs"
)

# user_auth.py web layer routes
@app.post("/api/oauth/login", response_model=LoginResonse, tags=["OAuth2 Authentication"])
async def login_authorization(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Authorization URL for OAuth2

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): Form Data
        db (Session, optional): Dependency Injection

    Returns:
        LoginResonse: Login Response
    """
    return await service_login_for_access_token(form_data, db)

@app.post("/api/oauth/token", response_model=GPTToken, tags=["OAuth2 Authentication"])
async def tokens_manager_oauth_codeflow(
    grant_type: str = Form(...),
    refresh_token: Optional[str] = Form(None),
    code: Optional[str] = Form(None)
):
    """
    Token URl For OAuth Code Grant Flow

    Args:
        grant_type (str): Grant Type
        code (Optional[str], optional)
        refresh_token (Optional[str], optional)

    Returns:
        access_token (str)
        token_type (str)
        expires_in (int)
        refresh_token (str)
    """
    return await gpt_tokens_service(grant_type, refresh_token, code)
    

# Get temp Code against user_id to implentent OAuth2 for Custom Gpt
@app.get("/api/oauth/temp-code", tags=["OAuth2 Authentication"])
async def get_temp_code(user_id: UUID):
    """
    Get Temp Code against user_id to implentent OAuth2 for Custom Gpt

    Args:
        user_id (UUID): User ID

    Returns:
        code (str): Temp Code
    """
    code = create_access_token(data={"id": user_id})
    return {"code": code}


@app.post("/api/oauth/signup", response_model=UserOutput, tags=["OAuth2 Authentication"])
async def signup_users(
    user_data: RegisterUser, db: Session = Depends(get_db)
):
    """
    Signup Users

    Args:
        user_data (RegisterUser): User Data
        db (Session, optional):  Dependency Injection

    Returns:
        UserOutput: User Output
    """
    return await service_signup_users(user_data, db)

#  todos_crud.py web layer routes

# Get ALL TODOS
@app.get("/api/todos", response_model=PaginatedTodos, tags=["TODO Crud"])
def get_todos(db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep), page: int = Query(1, description="Page number", ge=1),
              per_page: int = Query(10, description="Items per page", ge=1, le=100)):
    """
    Get ALL TODOS

    Args:
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection
        page (int, optional): Page number. Defaults to Query(1).
        per_page (int, optional): Items per page. Defaults to Query(10).

    Returns:

        PaginatedTodos: Paginated Todos
    """
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
    """
    Get a Single TODO item

    Args:
        todo_id (UUID): TODO ID
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        TODOResponse: TODO Response
    
    """
    try:
        return get_todo_by_id_service(todo_id, db, user_id)
    except HTTPException as e:
        # If the service layer raised an HTTPException, re-raise it
        raise e
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Create a new TODO item
@app.post("/api/todos", response_model=TODOResponse, tags=["TODO Crud"], status_code=201)
def create_todo(todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    """
    Create a new TODO item

    Args:
        todo (TODOBase): TODO Data
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        TODOResponse: TODO Response
    """
    try:
        return create_todo_service(todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Update a Single TODO item Completly
@app.put("/api/todos/{todo_id}", response_model=TODOResponse, tags=["TODO Crud"])
def update_todo(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    """
    Update a Single TODO item Completly

    Args:
        todo_id (UUID): TODO ID
        updated_todo (TODOBase): Updated TODO Data
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        TODOResponse: TODO Response
    """
    try:
        return full_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Update a Single TODO item partially
@app.patch("/api/todos/{todo_id}", response_model=TODOResponse, tags=["TODO Crud"])
def update_todo_partial(todo_id: UUID, updated_todo: TODOBase, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    """
    Partially Update a Single TODO item

    Args:
        todo_id (UUID): TODO ID
        updated_todo (TODOBase): Updated TODO Data
        db (Session, optional): Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        TODOResponse: TODO Response
    """
    try:
        return partial_update_todo_service(todo_id, updated_todo, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# DELETE a single TODO item
@app.delete("/api/todos/{todo_id}", tags=["TODO Crud"])
def delete_todo(todo_id: UUID, db: Session = Depends(get_db), user_id: UUID = Depends(get_current_user_dep)):
    """
    Delete a Single TODO item

    Args:
        todo_id (UUID): TODO ID
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        null
    """
    try:
        return delete_todo_data(todo_id, db, user_id)
    except Exception as e:
        # Handle specific exceptions with different HTTP status codes if needed
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")