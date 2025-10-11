from sqlalchemy.orm import Session
import secrets
import string
from datetime import datetime
from models.League import League
from models.LeagueMember import LeagueMember
from models.Squad import Squad
from models.SquadPlayer import SquadPlayer
from models.User import User
from ..schemas.league import LeagueCreate
from models.Competition import Competition

class LeagueService:
    @staticmethod
    def generate_join_code() -> str:
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    @staticmethod
    def generate_unique_join_code(db: Session) -> str:
        """Generate a join code that doesn't already exist"""
        while True:
            code = LeagueService.generate_join_code()
            # Check if this code already exists
            existing = db.query(League).filter(League.join_code == code).first()
            if not existing:
                return code
    
    @staticmethod
    def create_league(db: Session, league_data: LeagueCreate) -> League:
        join_code = LeagueService.generate_unique_join_code(db)

        # create the league object
        db_league = League(
            name=league_data.name,
            competition_id=league_data.competition_id,
            join_code=join_code,
            created_at=datetime.now()
        )

        try:
            db.add(db_league)
            db.commit()
            db.refresh(db_league)
            return db_league
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to create league: {str(e)}")
        
    @staticmethod
    def join_league(db: Session, join_code: str, user_id: int):
        possible_squad_positions = ["PR-S-1", "HK-S-1", "PR-S-2", "SR-S-1", "SR-S-2", "BR-S-1", "BR-S-2", "BR-S-3", "SH-S-1", "FH-S-1", "C-S-1", "C-S-2", "W-S-1", "W-S-2", "W-S-3", "PR-B-1", "PR-B-2", "HK-B-1", "BR-B-1", "SH-B-1", "FH-B-1", "C-B-1", "W-B-1"]

        # Find league by join code
        existing_league = db.query(League).filter(League.join_code == join_code).first()
        if not existing_league:
            raise ValueError("Invalid join code")
        
        # Check if league is locked
        if existing_league.is_locked:
            raise ValueError("League is locked")
        
        # Check if user already in league
        existing_membership = db.query(LeagueMember).filter(
            LeagueMember.user_id == user_id, 
            LeagueMember.league_id == existing_league.id
        ).first()
        if existing_membership:
            raise ValueError("User already in league")

        # Create membership
        db_league_membership = LeagueMember(
            user_id=user_id,
            league_id=existing_league.id
        )

        try:
            db.add(db_league_membership)
            db.flush() # Flush to get the league_member_id but doesn't commit

            db_initial_squad = Squad(
                user_id=user_id,
                league_member_id=db_league_membership.id
            )
            db.add(db_initial_squad)
            db.flush()
            for position in possible_squad_positions:
                _, squadRole, _ = position.split("-")  # Extract just the role (S/B)
                db.add(SquadPlayer(
                    squad_id=db_initial_squad.id,
                    squad_position=position,  # Store full position code like "FH-S-1"
                    is_starter=(squadRole == "S")
                ))
            db.commit()
            db.refresh(db_league_membership)
            return db_league_membership
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to join league: {str(e)}")
        
    @staticmethod
    def get_league_details(db: Session, league_id: int, user_id: int):
        # Find the league
        league = db.query(League).filter(League.id == league_id).first()
        if not league:
            raise ValueError("League not found")
        
        # Check if user is a member (only members can see details)
        membership = db.query(LeagueMember).filter(
            LeagueMember.league_id == league_id,
            LeagueMember.user_id == user_id
        ).first()
        if not membership:
            raise ValueError("You are not a member of this league")
        
        # Get all members with user info, ordered by position
        members_data = db.query(LeagueMember).join(User).filter(
            LeagueMember.league_id == league_id
        ).order_by(LeagueMember.position_in_league).all()
        
        # Format the response to match your schema
        return {
            "id": league.id,
            "name": league.name,
            "join_code": league.join_code,
            "competition_id": league.competition_id,
            "competition_name": league.competition.name,
            "is_locked": league.is_locked,
            "member_count": len(members_data),
            "members": [
                {
                    "id": member.id,
                    "username": member.user.username,
                    "points": member.points,
                    "position_in_league": member.position_in_league
                }
                for member in members_data
            ],
            "created_at": league.created_at
        }
    
    @staticmethod
    def get_my_league_memberships(db: Session, user_id: int):
        # Get all league memberships for the user with league and competition data
        print(user_id)
        memberships = db.query(LeagueMember).join(League).join(Competition).filter(
            LeagueMember.user_id == user_id
        ).all()
        
        # Format the response to match MyLeagueItem schema
        my_leagues = []
        for membership in memberships:
            # Count total members in this league
            member_count = db.query(LeagueMember).filter(
                LeagueMember.league_id == membership.league_id
            ).count()
            
            my_leagues.append({
                "id": membership.league.id,
                "name": membership.league.name,
                "competition_name": membership.league.competition.name,
                "member_count": member_count,
                "my_position": membership.position_in_league,
                "my_points": membership.points
            })
        
        return my_leagues

    @staticmethod
    def leave_league(db: Session, league_id: int, user_id: int):
        membership = db.query(LeagueMember).filter(
            LeagueMember.league_id == league_id,
            LeagueMember.user_id == user_id
        ).first()
        if not membership:
            raise ValueError("You are not a member of this league")
        
        try:
            db.delete(membership)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to leave league: {str(e)}")
