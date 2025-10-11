from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SquadPlayerInfo(BaseModel):
    id: int
    player_id: Optional[int] = None
    player_name: Optional[str] = None
    player_position: Optional[str] = None
    player_nation: Optional[str] = None
    squad_position: str
    is_starter: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class SquadDetailsResponse(BaseModel):
    id: int
    user_id: int
    league_member_id: int
    captain_id: Optional[int] = None
    vice_captain_id: Optional[int] = None
    kicker_id: Optional[int] = None
    backup_kicker_id: Optional[int] = None
    squad_players: List[SquadPlayerInfo]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransferRequest(BaseModel):
    player_in_id: int
    player_out_id: Optional[int] = None
    competition_round_id: int
    squad_position: str  # Squad position like "FH-S-1" or "FH-B-1". Can come from the ui
    
    class Config:
        from_attributes = True

class TransferResponse(BaseModel):
    id: int
    squad_id: int
    competition_round_id: int
    player_in_id: int
    player_out_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SelectSpecialPositionRequest(BaseModel):
    special_position: str  # "CAPTAIN", "VICE_CAPTAIN", "KICKER", "BACKUP_KICKER"
    player_id: int

    class Config:
        from_attributes = True

class SelectSpecialPositionResponse(BaseModel):
    id: int
    captain_id: Optional[int] = None
    vice_captain_id: Optional[int] = None
    kicker_id: Optional[int] = None
    backup_kicker_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True