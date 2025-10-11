from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.auth import get_current_user
from models.User import User
from ..schemas.squad import SquadDetailsResponse
from ..services.squad_service import SquadService
from ..services.scoring_service import ScoringService
from ..schemas.squad import TransferRequest, TransferResponse, SelectSpecialPositionRequest, SelectSpecialPositionResponse

router = APIRouter(prefix="/squads", tags=["squads"])

@router.get("/{squad_id}", response_model=SquadDetailsResponse)
def get_squad_details(
    squad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        squad_data = SquadService.get_squad_details(db, squad_id, current_user.id)
        return squad_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{squad_id}/{nation}")
def get_squad_players_from_nation(
    squad_id: int,
    nation: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        players = SquadService.get_squad_players_from_nation(db, squad_id, nation)
        return players
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/transfers/{squad_id}/{round_id}")
def get_squad_transfers_for_round(
    squad_id: int,
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        transfers = SquadService.get_squad_transfers_for_round(db, squad_id, round_id)
        return transfers
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/{squad_id}/transfer", response_model=TransferResponse)
def transfer_player(
    squad_id: int,
    transfer_data: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        transfer = SquadService.transfer_player(db, squad_id, transfer_data, current_user.id)
        return transfer
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/{squad_id}/select-special-position", response_model=SelectSpecialPositionResponse)
def select_special_position(
    squad_id: int,
    special_position_data: SelectSpecialPositionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        squad = SquadService.select_special_position(db, squad_id, special_position_data, current_user.id)
        return squad
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{squad_id}/calculate-score/{round_id}")
def calculate_squad_score(
    squad_id: int,
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        score_breakdown = ScoringService.calculate_squad_round_score(db, squad_id, round_id)
        return score_breakdown
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
