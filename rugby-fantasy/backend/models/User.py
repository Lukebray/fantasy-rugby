from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))  # Hashed passwords need space
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)  # Required field
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
