import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# 1) Read DATABASE_URL from env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2) Create engine & session factory (Render PostgreSQL needs sslmode)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3) Declare Base
Base = declarative_base()

# 4) Pull in your entire models package exactly once (respects __init__.py order)
import models   # noqa

def init_db():
    # 5) Auto-create all tables & indexes
    Base.metadata.create_all(bind=engine, checkfirst=True)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()