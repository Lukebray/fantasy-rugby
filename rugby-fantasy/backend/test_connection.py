from sqlalchemy import text
from app.database import engine

def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connected successfully!")
        # Check tables        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
        tables = result.fetchall()
        print("Tables:", [table[0] for table in tables])
        
if __name__ == "__main__":
    test_connection()