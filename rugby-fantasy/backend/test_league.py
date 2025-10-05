from models.League import League
from models.User import User
from models.LeagueMember import LeagueMember
from app.database import SessionLocal

def test_create_league_membership():
    db = SessionLocal()
    try:
        # Create a league
        league = League(name="testleague", join_code="JOIN")
        user = User(username="testuser", email="test@example.com", password="hashedpassword")
        db.add(league)
        db.add(user)
        db.commit()
        db.refresh(league)
        print(f"Created league: {league.id}, {league.name}")
        # Query it back        
        found_league = db.query(League).filter(League.name == "testleague").first()
        print(f"Found league: {found_league.name}, {found_league.join_code}")
        db.refresh(user)
        found_user = db.query(User).filter(User.username == "testuser").first()

        # Create a league membership
        league_membership = LeagueMember(user_id=found_user.id, league_id=found_league.id)
        db.add(league_membership)
        db.commit()
        db.refresh(league_membership)
        print(f"Created league membership: {league_membership.id}, {league_membership.user_id}, {league_membership.league_id}")
        
    finally:
        db.close()
if __name__ == "__main__":
    test_create_league_membership()