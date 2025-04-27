from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import SessionLocal, get_db, engine, Base
from core.middleware import RateLimitMiddleware
from models.admin_wallet import AdminWallet
import models  # ✅ Import all models once

from app.api.routes import router as api_router

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics.",
)

@app.on_event("startup")
def startup_event():
    # ✅ Initialize admin wallet
    db = SessionLocal()
    if not db.query(AdminWallet).first():
        db.add(AdminWallet(balance=0.00))
        db.commit()
    db.close()

# ✅ Ensure tables are created ONCE here after models are loaded
Base.metadata.create_all(bind=engine)

# Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)
