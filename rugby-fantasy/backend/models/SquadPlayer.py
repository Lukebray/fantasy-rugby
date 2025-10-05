from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class SquadPlayer(Base):
    __tablename__ = "squad_player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squad.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=False)
    is_starter: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))