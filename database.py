from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# IMPORT ALL MODELS HERE
from models.user import User
from models.deal import Deal
from models.share import Share
from models.wallet import Wallet
from models.admin import Admin
from models.escrow_tracker import EscrowTracker
from models.dispute import Dispute
from models.settings import AppSettings
from models.aiinsight import AIInsight

# Now create all tables
Base.metadata.create_all(bind=engine)
