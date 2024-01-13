from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Union
from jose import JWTError, jwt
from uuid import UUID
from dotenv import load_dotenv, find_dotenv
import os

from ..models._user_auth import TokenData, RegisterUser
from ..data._db_config import get_db
from ..utils._helpers import verify_password, credentials_exception, create_refresh_token, validate_refresh_token, get_current_user_dep
from ..data._user_auth import get_user, db_signup_users, InvalidUserException

_: bool = load_dotenv(find_dotenv())

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "30")
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get(
    "REFRESH_TOKEN_EXPIRE_MINUTES", "60")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for authentication")

if not ALGORITHM:
    raise ValueError("No ALGORITHM set for authentication")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db, username: str, password: str):
    """
    Authenticates a user by checking if the provided username and password match the stored credentials.

    Args:
        db: The database object used for querying user information.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        user: The authenticated user object if the credentials are valid, False otherwise.
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create an access token using the provided data and expiration delta.

    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (Union[timedelta, None], optional): The expiration delta for the access token.
            Defaults to None.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    # Convert UUID to string if it's present in the data
    if 'id' in to_encode and isinstance(to_encode['id'], UUID):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)

    to_encode.update({"exp": expire})

    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")

    if not isinstance(ALGORITHM, str):
        raise ValueError("ALGORITHM must be a string")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Get the current authenticated user based on the provided token.

    Args:
        token (str): The authentication token.
        db (Session): The database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        if not isinstance(SECRET_KEY, str):
            raise ValueError("SECRET_KEY must be a string")

        if not isinstance(ALGORITHM, str):
            raise ValueError("ALGORITHM must be a string")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Union[str, None] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def service_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    """
    Authenticates the user and generates an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the access token, token type, and user information.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
    )

    # Generate refresh token (you might want to set a longer expiry for this)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.username, "id": user.id}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "token_type": "bearer", "user": user, "expires_in": int(access_token_expires.total_seconds()), "refresh_token": refresh_token}


async def service_signup_users(
    user_data: RegisterUser, db: Session = Depends(get_db)
):
    """
    Service function to sign up users.

    Args:
        user_data (RegisterUser): The user data to be registered.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        The result of the user registration.

    Raises:
        HTTPException: If there is an invalid user exception or any other unforeseen exception.
    """
    try:
        return await db_signup_users(user_data, db)
    except InvalidUserException as e:
        # Catch the InvalidUserException and raise an HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Handle other unforeseen exceptions
        raise HTTPException(status_code=500, detail=str(e))


async def gpt_tokens_service(grant_type: str = Form(...), refresh_token: Optional[str] = Form(None), code: Optional[str] = Form(None)):
    """
    Generates access and refresh tokens based on the provided grant type.

    Args:
        grant_type (str): The grant type, either "refresh_token" or "authorization_code".
        refresh_token (str, optional): The refresh token used for token refresh flow.
        code (str, optional): The authorization code used for initial token generation flow.

    Returns:
        dict: A dictionary containing the access token, token type, expiry time, and refresh token.

    Raises:
        credentials_exception: If the grant type is invalid or the required parameters are missing.
    """
    # Token refresh flow
    if grant_type == "refresh_token":
        # Check if the refresh token is Present
        if not refresh_token:
            raise credentials_exception
        # Validate the refresh token and client credentials
        user_id = await validate_refresh_token(refresh_token)
        if not user_id:
            raise credentials_exception

    # Initial token generation flow
    elif grant_type == "authorization_code":
        user_id = await get_current_user_dep(code)
        if not user_id:
            raise credentials_exception
    else:
        raise credentials_exception

    # Generate access token
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"id": user_id}, expires_delta=access_token_expires)

    # Generate refresh token (you might want to set a longer expiry for this)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    rotated_refresh_token = create_refresh_token(data={"id": user_id}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "refresh_token": rotated_refresh_token  # Include refresh token in the response
    }
