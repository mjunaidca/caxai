from sqlmodel import Session, select
from typing import Union

from app.models import RegisterUser, USER
from app.utils import get_password_hash


class InvalidUserException(Exception):
    """
    Exception raised when a user is not found in the database.
    """

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def get_user(db: Session, username: Union[str, None] = None):

    if username is None:
        raise InvalidUserException(status_code=404, detail="Username not provided")

    user_query = select(USER).where(USER.username == username)
    user = db.exec(user_query).first()

    if not user:
        raise InvalidUserException(status_code=404, detail="User not found")
    print("user", user)
    return user


async def db_signup_users(
    user_data: RegisterUser, db: Session
):
    # Check if user already exists
    existing_user_email_query = select(USER).where((USER.email == user_data.email))
    existing_user_email = db.exec(existing_user_email_query).first()
    if existing_user_email:
        raise InvalidUserException(status_code=400, detail="Email already registered")
    
    existing_user_query = select(USER).where((USER.username == user_data.username))
    existing_user = db.exec(existing_user_query).first()
    if existing_user:
        raise InvalidUserException(status_code=400, detail="Username already registered")

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

