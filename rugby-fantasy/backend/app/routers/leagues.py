from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.auth import get_current_user
from models.User import User
from ..schemas.league import LeagueCreate, LeagueCreateResponse, LeagueJoin, LeagueJoinResponse, LeagueDetailsResponse, LeagueMemberInfo
from ..services.league_service import LeagueService

router = APIRouter(prefix="/leagues", tags=["leagues"])

@router.post("/", response_model=LeagueCreateResponse, status_code=status.HTTP_201_CREATED)
def create_league(
    league_data: LeagueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try: 
        league = LeagueService.create_league(db, league_data)
        return league
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/join", response_model=LeagueJoinResponse, status_code=status.HTTP_201_CREATED)
def join_league(
    league_join_data: LeagueJoin,  # Contains just join_code
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        league_membership = LeagueService.join_league(
            db, 
            league_join_data.join_code, 
            current_user.id
        )
        return league_membership
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{league_id}", response_model=LeagueDetailsResponse)
def get_league_details(
    league_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        league_data = LeagueService.get_league_details(db, league_id, current_user.id)
        return league_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

