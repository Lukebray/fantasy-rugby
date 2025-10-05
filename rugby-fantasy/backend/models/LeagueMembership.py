from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class LeagueMembership(Base):
    __tablename__ = "league_membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"), nullable=False)
    points: Mapped[int] = mapped_column(default=0)
    position_in_league: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))