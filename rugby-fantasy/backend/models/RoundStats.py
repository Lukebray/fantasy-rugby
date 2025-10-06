from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class RoundStats(Base):
    __tablename__ = "round_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition_round_id: Mapped[int] = mapped_column(ForeignKey("competition_round.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=False)
    # Rugby statistics
    tries: Mapped[int] = mapped_column(default=0)
    conversions: Mapped[int] = mapped_column(default=0)
    penalties: Mapped[int] = mapped_column(default=0)
    drop_goals: Mapped[int] = mapped_column(default=0)
    tackles: Mapped[int] = mapped_column(default=0)
    turnovers: Mapped[int] = mapped_column(default=0)
    lineout_wins: Mapped[int] = mapped_column(default=0)
    minutes_played: Mapped[int] = mapped_column(default=0)
    yellow_cards: Mapped[int] = mapped_column(default=0)
    red_cards: Mapped[int] = mapped_column(default=0)
    # Calculated fantasy points (based on above stats)
    fantasy_points: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    competition_round: Mapped["CompetitionRound"] = relationship("CompetitionRound", back_populates="round_stats")
    player: Mapped["Player"] = relationship("Player", back_populates="round_stats")