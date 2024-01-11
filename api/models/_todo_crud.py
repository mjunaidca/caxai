from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Union


class TODOBase(BaseModel):
    """
    Represents a TODO in the database.
    """
    title: str
    description: Union[str, None] = None
    completed: bool = False


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

    model_config = ConfigDict(from_attributes=True)


class PaginatedTodos(BaseModel):
    """
    Represents a paginated list of TODO items.
    """
    count: int
    next:  Union[str, None] = None
    previous:  Union[str, None] = None
    todos: list[TODOResponse]
