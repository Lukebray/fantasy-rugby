from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PlayerStatsResponse(BaseModel):
    id: int
    competition_round_id: int
    player_id: int
    tries: int
    conversions: int
    penalties: int
    drop_goals: int
    tackles: int
    turnovers: int
    lineout_wins: int
    minutes_played: int
    yellow_cards: int
    red_cards: int
    fantasy_points: int
    created_at: datetime
    
    class Config:
        from_attributes = True