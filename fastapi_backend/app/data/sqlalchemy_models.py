from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy import String, Boolean, UUID, DateTime, Text, func

import datetime
import uuid
class Base(DeclarativeBase):
    pass

class TODO(Base):
    
    """
    Represents a TODO in the database.
    """

    __tablename__ = "todos"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, index=True, nullable=True)  # Made description optional
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), index=True)


