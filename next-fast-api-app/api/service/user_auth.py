from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from typing import cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..models.user_auth import TokenData, RegisterUser
from ..data.db_config import get_db
from ..utils.helpers import verify_password
from ..data.user_auth import get_user, db_signup_users, InvalidUserException

from jose import JWTError, jwt

from uuid import UUID


from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for authentication")

if not ALGORITHM:
    raise ValueError("No ALGORITHM set for authentication")

if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise ValueError("No ACCESS_TOKEN_EXPIRE_MINUTES set for authentication")

# Explicitly annotate the type of ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_MINUTES = cast(str, ACCESS_TOKEN_EXPIRE_MINUTES)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # Convert UUID to string if it's present in the data
    if 'id' in to_encode and isinstance(to_encode['id'], UUID):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
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
    return {"access_token": access_token, "token_type": "bearer", "user": user}


async def service_signup_users(
    user_data: RegisterUser, db: Session = Depends(get_db)
):
    try:
        return await db_signup_users(user_data, db)
    except InvalidUserException as e:
        # Catch the InvalidUserException and raise an HTTPException
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Handle other unforeseen exceptions
        raise HTTPException(status_code=500, detail=str(e))
