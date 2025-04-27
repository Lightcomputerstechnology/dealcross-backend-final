import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# 1. Read DATABASE_URL from env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create engine & session factory with SSL mode for Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},  # Required for Render PostgreSQL
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Declare your Base
Base = declarative_base()

# 4. DB session dependency
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
