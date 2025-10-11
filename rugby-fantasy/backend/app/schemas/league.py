from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# This is the request body definition for creating a league
class LeagueCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="League Name")
    competition_id: int

# The response sent back after creating a league
class LeagueCreateResponse(BaseModel):
    id: int
    name: str
    join_code: str
    competition_id: int
    created_at: datetime

    class Config:
        from_attributes = True #telling pydantic to work with SQLAlchemy models

class LeagueJoin(BaseModel):
    join_code: str

class LeagueJoinResponse(BaseModel):
    id: int
    user_id: int
    league_id: int
    points: int
    position_in_league: int
    created_at: datetime

    class Config:
        from_attributes = True

class LeagueMemberInfo(BaseModel):
    id: int
    username: str
    points: int
    position_in_league: int
    
    class Config:
        from_attributes = True

class LeagueDetailsResponse(BaseModel):
    id: int
    name: str
    join_code: str
    competition_id: int
    competition_name: str
    is_locked: bool
    member_count: int
    members: List[LeagueMemberInfo]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MyLeagueItem(BaseModel):
    id: int
    name: str
    competition_name: str
    member_count: int
    my_position: int
    my_points: int

    class Config:
        from_attributes = True
