from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class League(Base):
    __tablename__ = "league"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    join_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    is_locked: Mapped[bool] = mapped_column(default=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    competition: Mapped["Competition"] = relationship("Competition", back_populates="leagues")
    members: Mapped[List["LeagueMember"]] = relationship("LeagueMember", back_populates="league")