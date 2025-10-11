from sqlalchemy.orm import Session
import string
from datetime import datetime
from models.Squad import Squad
from models.SquadPlayer import SquadPlayer
from models.Player import Player
from models.Transfer import Transfer
from models.CompetitionRound import CompetitionRound
from .competition_service import CompetitionService
from ..schemas.squad import SelectSpecialPositionRequest
from ..schemas.squad import TransferRequest

class SquadService:
    @staticmethod
    def get_squad_details(db: Session, squad_id: int, user_id: int):
        # Find the squad
        squad = db.query(Squad).filter(Squad.id == squad_id).first()
        if not squad:
            raise ValueError("Squad not found")
        
        # Check if user is a member (only members can see details)
        if squad.user_id != user_id:
            raise ValueError("You are not a member of this squad")
        
        # Get all squad players (including empty slots)
        squad_players_data = db.query(SquadPlayer).filter(
            SquadPlayer.squad_id == squad_id
        ).all()

        # Format the response to match your schema
        return {
            "id": squad.id,
            "user_id": squad.user_id,
            "league_member_id": squad.league_member_id,
            "captain_id": squad.captain_id,
            "vice_captain_id": squad.vice_captain_id,
            "kicker_id": squad.kicker_id,
            "backup_kicker_id": squad.backup_kicker_id,
            "squad_players": [
                {
                    "id": squad_player.id,
                    "player_id": squad_player.player_id,
                    "player_name": squad_player.player.name if squad_player.player else None,
                    "player_position": squad_player.player.position if squad_player.player else None,
                    "player_nation": squad_player.player.nation if squad_player.player else None,
                    "squad_position": squad_player.squad_position,
                    "is_starter": squad_player.is_starter,
                    "created_at": squad_player.created_at
                }
                for squad_player in squad_players_data
            ],
            "created_at": squad.created_at
        }


    @staticmethod
    def get_squad_players_from_nation(db: Session, squad_id: int, nation: str):
        # Get count of players from specific nation in the squad
        count = db.query(SquadPlayer).join(Player).filter(
            SquadPlayer.squad_id == squad_id,
            Player.nation == nation,
            SquadPlayer.player_id.isnot(None)  # Only count filled positions
        ).count()
        return count
    
    @staticmethod
    def get_squad_transfers_for_round(db: Session, squad_id: int, round_id: int):
        transfers = db.query(Transfer).filter(
            Transfer.squad_id == squad_id,
            Transfer.competition_round_id == round_id
        ).all()
        return transfers
    
    @staticmethod
    def validate_transfer(db: Session, squad_id,transfer_data: TransferRequest):
        # Get the actual Player objects
        player_in = db.query(Player).filter(Player.id == transfer_data.player_in_id).first()
        if not player_in:
            raise ValueError("Player in not found")

        player_out = None
        if transfer_data.player_out_id:
            player_out = db.query(Player).filter(Player.id == transfer_data.player_out_id).first()
            if not player_out:
                raise ValueError("Player out not found")

        # Check nation limit (only if adding a new nation to squad)
        current_nation_count = SquadService.get_squad_players_from_nation(db, squad_id, player_in.nation)

        # If replacing player from same nation, no nation limit issue
        # If replacing player from different nation, or adding to empty slot, check limit
        if not player_out or player_out.nation != player_in.nation:
            if current_nation_count >= 6:
                raise ValueError(f"Squad already has 6 players from {player_in.nation}")
            
        # Check if transfer deadline has passed
        transfer_deadline = CompetitionService.get_round_transfer_deadline(db, transfer_data.competition_round_id)
        if datetime.now() > transfer_deadline:
            raise ValueError("Transfer deadline has passed")

        # Check if transfer limit is reached
        transfers_for_round = SquadService.get_squad_transfers_for_round(db, squad_id, transfer_data.competition_round_id)
        competition_round = db.query(CompetitionRound).filter(CompetitionRound.id == transfer_data.competition_round_id).first()
        if not competition_round:
            raise ValueError("Competition round not found")

        if len(transfers_for_round) >= competition_round.transfer_limit:
            raise ValueError("Transfer limit reached")

        # Check if player position matches squad position
        required_position = transfer_data.squad_position.split("-")[0]  # "FH-S-1" -> "FH"
        if player_in.position != required_position:
            raise ValueError(f"Player position {player_in.position} doesn't match required position {required_position}")

        return True
        
    @staticmethod
    def transfer_player(db: Session, squad_id: int, transfer_data: TransferRequest, user_id: int):
        # Check if user owns the squad
        squad = db.query(Squad).filter(Squad.id == squad_id).first()
        if not squad:
            raise ValueError("Squad not found")
        if squad.user_id != user_id:
            raise ValueError("You are not authorized to modify this squad")

        # Check if this is a rearrangement (player already in squad) or a transfer (new player)
        existing_squad_player = db.query(SquadPlayer).filter(
            SquadPlayer.squad_id == squad_id,
            SquadPlayer.player_id == transfer_data.player_in_id
        ).first()

        if existing_squad_player:
            # This is a rearrangement - swap positions
            return SquadService._handle_rearrangement(db, squad_id, transfer_data, existing_squad_player)
        else:
            # This is a transfer - validate and create transfer record
            if SquadService.validate_transfer(db, squad_id, transfer_data):
                # Update the squad position
                target_squad_player = db.query(SquadPlayer).filter(
                    SquadPlayer.squad_id == squad_id,
                    SquadPlayer.squad_position == transfer_data.squad_position
                ).first()

                if not target_squad_player:
                    raise ValueError("Squad position not found")

                target_squad_player.player_id = transfer_data.player_in_id

                # Create transfer record
                db_transfer = Transfer(
                    squad_id=squad_id,
                    competition_round_id=transfer_data.competition_round_id,
                    player_in_id=transfer_data.player_in_id,
                    player_out_id=transfer_data.player_out_id
                )
                db.add(db_transfer)
                db.commit()
                db.refresh(db_transfer)
                return db_transfer

    @staticmethod
    def _handle_rearrangement(db: Session, squad_id: int, transfer_data: TransferRequest, moving_squad_player: SquadPlayer):
        # Find the target position
        target_squad_player = db.query(SquadPlayer).filter(
            SquadPlayer.squad_id == squad_id,
            SquadPlayer.squad_position == transfer_data.squad_position
        ).first()

        if not target_squad_player:
            raise ValueError("Target squad position not found")

        # Validate position compatibility for the moving player
        if moving_squad_player.player:
            required_position = transfer_data.squad_position.split("-")[0]
            if moving_squad_player.player.position != required_position:
                raise ValueError(f"Player position {moving_squad_player.player.position} doesn't match required position {required_position}")

        # Swap the positions
        old_position = moving_squad_player.squad_position
        moving_squad_player.squad_position = target_squad_player.squad_position
        target_squad_player.squad_position = old_position

        # Update is_starter based on new positions
        moving_squad_player.is_starter = (moving_squad_player.squad_position.split("-")[1] == "S")
        target_squad_player.is_starter = (target_squad_player.squad_position.split("-")[1] == "S")

        db.commit()

        # Return a mock TransferResponse for rearrangements (no actual transfer record)
        from datetime import datetime, timezone
        return {
            "id": -1,  # Negative ID to indicate this is a rearrangement, not a real transfer
            "squad_id": squad_id,
            "competition_round_id": transfer_data.competition_round_id,
            "player_in_id": transfer_data.player_in_id,
            "player_out_id": target_squad_player.player_id,  # The player that was swapped
            "created_at": datetime.now(timezone.utc)
        }

    @staticmethod
    def select_special_position(db: Session, squad_id: int, special_position_data: SelectSpecialPositionRequest, user_id: int):
        # Check if user owns the squad
        squad = db.query(Squad).filter(Squad.id == squad_id).first()
        if not squad:
            raise ValueError("Squad not found")
        if squad.user_id != user_id:
            raise ValueError("You are not authorized to modify this squad")

        if special_position_data.special_position == "CAPTAIN":
            squad.captain_id = special_position_data.player_id
        elif special_position_data.special_position == "VICE_CAPTAIN":
            squad.vice_captain_id = special_position_data.player_id
        elif special_position_data.special_position == "KICKER":
            squad.kicker_id = special_position_data.player_id
        elif special_position_data.special_position == "BACKUP_KICKER":
            squad.backup_kicker_id = special_position_data.player_id
        else:
            raise ValueError("Invalid special position")

        db.commit()
        db.refresh(squad)
        return squad

