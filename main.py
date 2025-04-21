# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine

# Core routers
from routers import auth, wallet, deals, disputes, admin

# Admin feature routers
from app.api.routes import (
    analytics,
    charts,
    fraud,
    auditlog,
    dealcontrol,
    usercontrol
)
from routers import secure_admin  # ✅ NEW router for protected admin features

# Initialize DB tables (auto-create)
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend powering the Dealcross platform including escrow, analytics, fraud detection, admin controls, and more.",
)

# CORS config (You can lock this to frontend origin later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Public API Routes ===
app.include_router(auth.router,       prefix="/auth",     tags=["Authentication"])
app.include_router(wallet.router,     prefix="/wallet",   tags=["Wallet"])
app.include_router(deals.router,      prefix="/deals",    tags=["Deals"])
app.include_router(disputes.router,   prefix="/disputes", tags=["Disputes"])

# === Admin API Routes ===
app.include_router(admin.router,        prefix="/admin", tags=["Admin Core"])
app.include_router(analytics.router,    prefix="/admin", tags=["Admin Analytics"])
app.include_router(charts.router,       prefix="/admin", tags=["Admin Charts"])
app.include_router(fraud.router,        prefix="/admin", tags=["Fraud Reports"])
app.include_router(auditlog.router,     prefix="/admin", tags=["Audit Logs"])
app.include_router(dealcontrol.router,  prefix="/admin", tags=["Pending Deals"])
app.include_router(usercontrol.router,  prefix="/admin", tags=["User Controls"])
app.include_router(secure_admin.router, prefix="/admin", tags=["Admin Secure"])  # ✅ Added here
