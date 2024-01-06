from pydantic import BaseModel
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class RegisterUser(User):
    password: str


class UserInDB(User):
    id: UUID
    hashed_password: str

class UserOutput(User):
    id: UUID

class LoginResonse(Token):
    user: UserOutput
