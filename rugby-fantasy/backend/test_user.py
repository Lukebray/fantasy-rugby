from models.User import User
from app.database import SessionLocal

def test_create_user():
    db = SessionLocal()
    try:
        # Create a user        user = User(username="testuser", email="test@example.com", password="hashedpassword")
        user = User(username="testuser", email="test@example.com", password="hashedpassword")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user: {user.id}, {user.username}")
        # Query it back        
        found_user = db.query(User).filter(User.username == "testuser").first()
        print(f"Found user: {found_user.username}, {found_user.email}")
    finally:
        db.close()
if __name__ == "__main__":
    test_create_user()