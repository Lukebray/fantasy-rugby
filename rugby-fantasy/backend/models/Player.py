from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    position: Mapped[str] = mapped_column(String(32))  # e.g. "PR", "FL", "SH", "FB"
    nation: Mapped[str] = mapped_column(String(32))  # e.g. "IRE", "ENG", "FRA", "SCO", "WAL", "ITA"
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))