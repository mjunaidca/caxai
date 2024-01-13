from typing import Union
from sqlalchemy.orm import Session

from ._sqlalchemy_models import USER
from ..models._user_auth import  RegisterUser
from ..utils._helpers import get_password_hash

class InvalidUserException(Exception):
    """
    Exception raised when a user is not found in the database.
    """
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def get_user(db, username: Union[str, None] = None):

    if username is None:
        raise InvalidUserException(status_code=404, detail="Username not provided")

    user = db.query(USER).filter(USER.username == username).first()
    
    if not user:
        raise InvalidUserException(status_code=404, detail="User not found")
    print("user", user)
    return user


async def db_signup_users(
    user_data: RegisterUser, db: Session
):
    # Check if user already exists
    existing_user = db.query(USER).filter((USER.username == user_data.username) | (USER.email == user_data.email)).first()
    if existing_user:
        raise InvalidUserException(status_code=400, detail="Email or username already registered")

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create new user instance
    new_user = USER(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
    )

    # Add new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the new user data
    return new_user