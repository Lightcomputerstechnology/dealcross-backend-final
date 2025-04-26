# File: core/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# 1. Read DATABASE_URL from env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create engine & session factory
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Declare your base
Base = declarative_base()

# 4. Auto-create all tables & indexes at startup
def init_db():
    """
    Auto-create tables for all models bound to Base metadata.
    Call this on application startup.
    """
    Base.metadata.create_all(bind=engine, checkfirst=True)

# 5. DB session dependency
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()