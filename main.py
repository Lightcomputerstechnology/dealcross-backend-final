from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import SessionLocal, engine, Base
from core.middleware import RateLimitMiddleware

# Import all models here to register them with SQLAlchemy
from models.user import User
from models.kyc import KYCRequest
from models.wallet import Wallet
from models.admin_wallet import AdminWallet

from app.api.routes import router as api_router

# Initialize FastAPI app
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics."
)

# Ensure database tables are created (only missing tables)
Base.metadata.create_all(bind=engine)

# Initialize Admin Wallet on startup (if not exists)
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if not db.query(AdminWallet).first():
            db.add(AdminWallet(balance=0.00))
            db.commit()
    finally:
        db.close()

# Middleware: Rate limiting and CORS
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)
