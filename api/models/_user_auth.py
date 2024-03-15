from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from api.models._todo_crud import TODO
class Token(SQLModel):
    access_token: str
    token_type: str

class GPTToken(Token):
    expires_in: int
    refresh_token: str



class TokenData(SQLModel):
    username: Union[str, None] = None

class User(SQLModel):
    username: str = Field( unique=True, index=True)
    email: str = Field( unique=True, index=True)
    full_name: str = Field()
    email_verified: Union[bool, None] = None


class USER(SQLModel, table=True):
    """
    Represents a User in the database.
    """

    id: UUID | None = Field(primary_key=True, index=True, default_factory=uuid4)
    hashed_password: str = Field( index=True)
    email_verified: bool = Field(default=False)

    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    created_at: datetime | None = Field(default_factory=datetime.now)

    # Relationship to reference the todos
    todos: Optional[list["TODO"]] = Relationship(back_populates="user")


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