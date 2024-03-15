from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, Union

from api.models._user_auth import USER


class TODOBase(SQLModel):
    """
    Represents a TODO in the database.
    """
    title: str = Field(index=True)
    description: str = Field(default=None, nullable=True)  # Made description optional
    completed: bool = Field(default=False)

class TODO(TODOBase, table=True):
    """
    Represents a TODO in the database.
    """

    id: UUID | None = Field(primary_key=True, index=True, default_factory=uuid4)
    
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    created_at: datetime | None = Field(default_factory=datetime.now)
    # Foreign key to reference the user
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    user: Optional["USER"] = Relationship(back_populates="todos")


class TODOCreate(TODOBase):
    """
    Represents a TODO item to be created.
    """
    id: UUID


class TODOResponse(TODOBase):
    """
    Represents a TODO item to be returned.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID


class PaginatedTodos(SQLModel):
    """
    Represents a paginated list of TODO items.
    """
    count: int
    next:  Union[str, None] = None
    previous:  Union[str, None] = None
    todos: list[TODOResponse]
