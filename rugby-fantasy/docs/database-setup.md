# Database Setup Guide

This guide walks you through setting up PostgreSQL with Docker and creating your first database migration.

## Prerequisites
- Docker installed and running
- Poetry environment set up in `backend/`
- DBeaver (or similar database client) for viewing data

## Step 1: Create PostgreSQL Docker Container

```bash
docker run --name rugby-fantasy-postgres \
  -e POSTGRES_DB=rugby_fantasy \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15
```

**Verify it's running:**
```bash
docker ps
```
You should see `rugby-fantasy-postgres` in the list.

## Step 2: Connect with DBeaver

Create a new PostgreSQL connection with these settings:
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `rugby_fantasy`
- **Username:** `postgres`
- **Password:** `password`

Test the connection - you should see an empty database.

## Step 3: Set Up Database Configuration

Create `backend/app/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost:5432/rugby_fantasy"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Step 4: Initialize Alembic

```bash
cd backend
poetry run alembic init alembic
```

This creates an `alembic/` directory with migration files.

## Step 5: Configure Alembic

### Edit `backend/alembic.ini`
Find the line with `sqlalchemy.url` and change it to:
```ini
sqlalchemy.url = postgresql://postgres:password@localhost:5432/rugby_fantasy
```

### Edit `backend/alembic/env.py`
Add these imports at the top:
```python
from models.User import Base
```

Find the line `target_metadata = None` and change it to:
```python
target_metadata = Base.metadata
```

## Step 6: Create Your First Migration

```bash
cd backend
poetry run alembic revision --autogenerate -m "Create user table"
```

This creates a migration file in `alembic/versions/`.

## Step 7: Run the Migration

```bash
poetry run alembic upgrade head
```

## Step 8: Verify in DBeaver

Refresh your DBeaver connection. You should now see:
- A `user` table with columns: id, username, password, email
- An `alembic_version` table (tracks migrations)

## Step 9: Test Database Connection

Create `backend/test_connection.py`:

```python
from sqlalchemy import text
from app.database import engine

def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connected successfully!")
        
        # Check tables
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
        tables = result.fetchall()
        print("Tables:", [table[0] for table in tables])

if __name__ == "__main__":
    test_connection()
```

Run it:
```bash
poetry run python test_connection.py
```

## Step 10: Test Creating a User

Create `backend/test_user.py`:

```python
from models.User import User
from app.database import SessionLocal

def test_create_user():
    db = SessionLocal()
    try:
        # Create a user
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
```

Run it:
```bash
poetry run python test_user.py
```

Check DBeaver - you should see the new user in the `user` table!

## Common Issues

### "Connection reset" in DBeaver
- Check if Docker container is running: `docker ps`
- Start container if stopped: `docker start rugby-fantasy-postgres`
- Check container logs: `docker logs rugby-fantasy-postgres`

### "alembic command not found"
- Always use `poetry run alembic` instead of just `alembic`
- Make sure you're in the `backend/` directory

### Migration doesn't detect changes
- Make sure your model imports `Base` from the same place as `alembic/env.py`
- Check that `target_metadata = Base.metadata` is set correctly

## Next Steps

Once this is working, you can:
1. Add more models (League, Player, etc.)
2. Create new migrations with `poetry run alembic revision --autogenerate -m "description"`
3. Always run `poetry run alembic upgrade head` to apply migrations
4. Use DBeaver to inspect your data as you develop

## Useful Commands

```bash
# Check current migration version
poetry run alembic current

# See migration history
poetry run alembic history

# Downgrade one migration
poetry run alembic downgrade -1

# Reset database (careful!)
docker stop rugby-fantasy-postgres
docker rm rugby-fantasy-postgres
# Then recreate with Step 1
```
