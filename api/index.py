from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Query, Form
from fastapi.security import OAuth2PasswordRequestForm

from uuid import UUID
from datetime import timedelta

# Now you can use relative imports
from .data._db_config import get_db
from .models._user_auth import RegisterUser, UserOutput, LoginResonse, GPTToken
from .service._user_auth import service_signup_users, service_login_for_access_token, create_access_token
from .data._db_config import get_db
from .models._todo_crud import TODOBase, TODOResponse, PaginatedTodos
from .service._todos_crud import create_todo_service, get_todo_by_id_service, get_all_todos_service, full_update_todo_service, partial_update_todo_service, delete_todo_data
from .utils._helpers import get_current_user_dep, create_refresh_token

app = FastAPI(
    title="Cal AI",
    description="A multi-user to-do application for efficient task management.",
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
    ]
)

# user_auth.py web layer routes
@app.post("/api/auth/login", response_model=LoginResonse, tags=["Authentication"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return await service_login_for_access_token(form_data, db)

# Get Access Token against user_id encoded temp token
@app.post("/api/token", response_model=GPTToken, tags=["Authentication"])
async def get_access_token(code: Annotated[str, Form()]):
    user_id = await get_current_user_dep(code)

    print('user_id', user_id)

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    # Define token expiration times
    access_token_expires = timedelta(minutes=float(3))
    # refresh_token_expires = timedelta(days=7)

    access_token = create_access_token(data={"id": user_id}, expires_delta=access_token_expires)
    
    """ 
    https://community.openai.com/t/guide-how-oauth-refresh-tokens-revocation-work-with-gpt-actions/533147 
    If GPT expires the token by adding expire time then I will create this part of flow later when adding
    forgot password, email code validation in OAuth2 flow for GPT and web app
    """
    # refresh_token = create_refresh_token(data={"id": user_id}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": int(access_token_expires.total_seconds())
    }

# Get temp Code against user_id to implentent OAuth2 for Custom Gpt
@app.get("/api/auth/temp-code", tags=["Authentication"])
async def get_temp_code(user_id: UUID):
    code = create_access_token( data={"id": user_id})
    return {"code": code}



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


# https://caxgpt.vercel.app/auth/login?response_type=code&client_id=&redirect_uri=https%3A%2F%2Fchat.openai.com%2Faip%2Fg-3e0e5b8cffe6595098a7030d91a9502af4a89130%2Foauth%2Fcallback&scope=&state=92497294-3eb3-452c-813d-53c8e2c4b923

    # Sign in to register
# https://caxgpt.vercel.app/auth/register?redirect_uri=https://chat.openai.com/aip/g-3e0e5b8cffe6595098a7030d91a9502af4a89130/oauth/callback&state=92497294-3eb3-452c-813d-53c8e2c4b923&response_type=code&client_id=&scope=