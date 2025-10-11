from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.auth import get_current_user
from models.User import User
from ..services.competition_service import CompetitionService

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/round/{round_id}/transfer-deadline")
def get_round_transfer_deadline(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        deadline = CompetitionService.get_round_transfer_deadline(db, round_id)
        return deadline
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
