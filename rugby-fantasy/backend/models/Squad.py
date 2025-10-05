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