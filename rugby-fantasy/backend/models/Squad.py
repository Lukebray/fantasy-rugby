from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class Squad(Base):
    __tablename__ = "squad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    league_member_id: Mapped[int] = mapped_column(ForeignKey("league_membership.id"), nullable=False)
    captain_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=True)
    vice_captain_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=True)
    kicker_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=True)
    backup_kicker_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="squads")
    league_member: Mapped["LeagueMember"] = relationship("LeagueMember", back_populates="squad")
    captain: Mapped["Player"] = relationship("Player", foreign_keys=[captain_id])
    vice_captain: Mapped["Player"] = relationship("Player", foreign_keys=[vice_captain_id])
    kicker: Mapped["Player"] = relationship("Player", foreign_keys=[kicker_id])
    backup_kicker: Mapped["Player"] = relationship("Player", foreign_keys=[backup_kicker_id])
    squad_players: Mapped[List["SquadPlayer"]] = relationship("SquadPlayer", back_populates="squad")
    transfers: Mapped[List["Transfer"]] = relationship("Transfer", back_populates="squad")