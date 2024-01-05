from pydantic import BaseModel
from uuid import UUID

class TODOBase(BaseModel):
    """
    Represents a TODO in the database.
    """
    title: str
    description: str
    completed: bool = False

class TODOCreate(TODOBase):
    """
    Represents a TODO item to be created.
    """
    id: UUID