from sqlalchemy.orm import Session
import string
from datetime import datetime
from models.Competition import Competition
from models.CompetitionRound import CompetitionRound

class CompetitionService:
    @staticmethod
    def get_round_transfer_deadline(db: Session, round_id: int):
        round = db.query(CompetitionRound).filter(CompetitionRound.id == round_id).first()
        if not round:
            raise ValueError("Round not found")
        return round.transfer_deadline