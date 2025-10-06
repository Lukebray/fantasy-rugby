from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class CompetitionRound(Base):
    __tablename__ = "competition_round"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"), nullable=False)
    round_number: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    transfer_deadline: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    competition: Mapped["Competition"] = relationship("Competition", back_populates="rounds")
    round_stats: Mapped[List["RoundStats"]] = relationship("RoundStats", back_populates="competition_round")
    transfers: Mapped[List["Transfer"]] = relationship("Transfer", back_populates="competition_round")