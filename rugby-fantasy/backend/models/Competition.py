from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    leagues: Mapped[List["League"]] = relationship("League", back_populates="competition")
    rounds: Mapped[List["CompetitionRound"]] = relationship("CompetitionRound", back_populates="competition")