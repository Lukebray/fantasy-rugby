from sqlalchemy.orm import Session
from models.RoundStats import RoundStats
from models.CompetitionRound import CompetitionRound
from models.Player import Player

class StatsService:
    @staticmethod
    def get_player_stats_for_round(db: Session, player_id: int, round_id: int):
        player_stats = db.query(RoundStats).filter(
            RoundStats.player_id == player_id,
            RoundStats.competition_round_id == round_id
        ).first()
        return player_stats
