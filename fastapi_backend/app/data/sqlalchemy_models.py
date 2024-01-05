from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy import String, Boolean, UUID, DateTime, func

class Base(DeclarativeBase):
    pass

class TODO(Base):
    
    """
    Represents a TODO in the database.
    """

    __tablename__ = "todos"
    id = mapped_column(UUID, primary_key=True, index=True)
    title = mapped_column(String, index=True)
    description = mapped_column(String, index=True)
    completed = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=func.now(), index=True)
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now(), index=True)