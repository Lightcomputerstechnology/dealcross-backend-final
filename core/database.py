# core/database.py
from tortoise import Tortoise
from config import settings  # Use your existing Pydantic settings
import os

# DATABASE URL for Tortoise ORM (replace with your actual environment variable)
DATABASE_URL = os.getenv("DATABASE_URL")  # This is already stored in the environment

# Initialize the database (Tortoise ORM)
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,  # Pull DATABASE_URL from environment settings
        modules={"models": ["models"]}  # Tells Tortoise where your models live
    )
    await Tortoise.generate_schemas()  # Optionally auto-create tables (if using Aerich, skip this part)

# Close DB connection
async def close_db():
    await Tortoise.close_connections()

# Session management (not needed for Tortoise ORM directly, but included for SQLAlchemy compatibility)
# If you still want SQLAlchemy, you can leave this out, but we're shifting towards Tortoise ORM.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy setup (only for compatibility or if needed)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine with SSL (Render PostgreSQL requires this)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

# SQLAlchemy SessionLocal and Base setup (if using SQLAlchemy models elsewhere)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for SQLAlchemy DB session (if you continue using SQLAlchemy in some places)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()