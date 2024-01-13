from pydantic import BaseModel
from uuid import UUID
from typing import Union
class Token(BaseModel):
    access_token: str
    token_type: str

class GPTToken(Token):
    expires_in: int
    refresh_token: str



class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    email_verified: Union[bool, None] = None

class RegisterUser(User):
    password: str


class UserInDB(User):
    id: UUID
    hashed_password: str

class UserOutput(User):
    id: UUID

class LoginResonse(Token):
    user: UserOutput
    expires_in: int
    refresh_token: str