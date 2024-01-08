from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer
from fastapi import Security
from dotenv import load_dotenv, find_dotenv
import os
from uuid import UUID
from fastapi import HTTPException, status
from typing import Union
_: bool = load_dotenv(find_dotenv())

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "30")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for authentication")

if not ALGORITHM:
    raise ValueError("No ALGORITHM set for authentication")

if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise ValueError("No ACCESS_TOKEN_EXPIRE_MINUTES set for authentication")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user_dep(token: str = Security(oauth2_scheme)) -> Union[str, UUID]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID = UUID(payload.get("id"))
        # You can add more user-related validation here if needed
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
