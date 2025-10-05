from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .User import Base

class Transfer(Base):
    __tablename__ = "transfer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squad.id"), nullable=False)
    competition_round_id: Mapped[int] = mapped_column(ForeignKey("competition_round.id"), nullable=False)
    player_in_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=False)
    player_out_id: Mapped[int] = mapped_column(ForeignKey("player.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))