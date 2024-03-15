from typing import Annotated, Optional
from sqlmodel import Session

from fastapi import Depends, FastAPI, Form
from fastapi.security import OAuth2PasswordRequestForm

from uuid import UUID
from contextlib import asynccontextmanager

# Now you can use relative imports
from app.models import RegisterUser, UserOutput, LoginResonse, GPTToken
from app.core.config_db import get_db, create_db_and_tables
from app.service import service_signup_users, service_login_for_access_token, create_access_token, gpt_tokens_service
from app.core.utils import get_current_user_dep

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Cax Auth Server",
    description="Auth Service for multi-user to-do microservice",
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
            "url": "http://localhost:8080",
            "description": "Development server"
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

# Endpoint that takes token and returns user data
@app.get("/api/users/me", tags=["User"])
async def read_users_me(user_id: UUID = Depends(get_current_user_dep)):
    """
    Get Current User

    Args:
        current_user (UserOutput, optional):  Dependency Injection

    Returns:
        UserOutput: User Output
    """
    return user_id