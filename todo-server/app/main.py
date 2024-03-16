from fastapi import Depends, FastAPI, HTTPException, Query, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from uuid import UUID
from typing import Annotated
from contextlib import asynccontextmanager
import httpx

# Now you can use relative imports
from app.core.config_db import get_db, create_db_and_tables
from app.core.settings import AUTH_SERVER_URL
from app.models import TODOBase, TODOResponse, PaginatedTodos
from app.service import create_todo_service, get_todo_by_id_service, get_all_todos_service, full_update_todo_service, partial_update_todo_service, delete_todo_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("Creating Tables")
    # create_db_and_tables()
    yield


app = FastAPI(
    # lifespan=lifespan,
    title="Cax",
    description="A multi-user to-do microservice for efficient task management.",
    version="1.0.0",
    terms_of_service="https://cax.vercel.app/terms/",
    contact={
        "name": "Muhammad Junaid",
        "url": "https://www.linkedin.com/in/mrjunaid/",
        "email": "mr.junaidshaukat@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    docs_url="/api/docs"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Call Auth Server and get str user_id owith 200 or an error message in JSON - use httpx 
def get_current_user_dep(token: Annotated[str | None, Depends(oauth2_scheme)]):
    print("get_user_id token", token)
    print("\n-------\n\\\\\\\\-n  AUTH_SERVER_URL", AUTH_SERVER_URL)
    url = f"{AUTH_SERVER_URL}/api/users/me"
    headers = {"Authorization": f"Bearer {token}"}

    response = httpx.get(url, headers=headers)

    print( "get_user_id" ,response.json())

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json().get('detail'))

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Get ALL TODOS
@app.get("/api/todos", response_model=PaginatedTodos, tags=["TODO Crud"])
def get_todos(db: Session = Depends(get_db), user_id = Depends(get_current_user_dep), page: int = Query(1, description="Page number", ge=1),
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
        print("\n IN API ROUTE user_id", user_id)
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