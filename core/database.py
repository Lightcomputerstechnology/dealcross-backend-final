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

# — ensure all models are imported so Base.metadata sees them —
import models.user
import models.deal
import models.wallet
import models.share
import models.dispute
import models.escrow_tracker
import models.settings
import models.aiinsight
import models.fee_transaction
import models.admin_wallet
import models.kyc
import models.fraud
import models.audit
import models.notification
import models.wallet_transaction

# 4. Auto-create all tables & indexes at startup
def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)

# 5. DB session dependency
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()