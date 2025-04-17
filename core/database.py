from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import os

# ▶ 1.  read the DATABASE_URL from Render’s env‑vars
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# ▶ 2.  SQLAlchemy boiler‑plate
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ▶ 3.  FastAPI dependency for DB sessions
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
