# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine

# Core routers
from routers import auth, wallet, deals, disputes, admin, kyc  # ✅ Added kyc

# Admin feature routers
from app.api.routes import (
    analytics,
    charts,
    fraud,
    auditlog,
    dealcontrol,
    usercontrol,
)
from routers import secure_admin  # ✅ Admin-protected route

# Initialize all tables
Base.metadata.create_all(bind=engine)

# FastAPI app configuration
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend powering the Dealcross platform including escrow, analytics, fraud detection, admin controls, and more.",
)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with frontend domain before production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Public API Routes ===
app.include_router(auth.router,       prefix="/auth",     tags=["Authentication"])
app.include_router(wallet.router,     prefix="/wallet",   tags=["Wallet"])
app.include_router(deals.router,      prefix="/deals",    tags=["Deals"])
app.include_router(disputes.router,   prefix="/disputes", tags=["Disputes"])
app.include_router(kyc.router,        prefix="/kyc",      tags=["KYC Verification"])  # ✅ NEW

# === Admin API Routes ===
app.include_router(admin.router,        prefix="/admin", tags=["Admin Core"])
app.include_router(analytics.router,    prefix="/admin", tags=["Admin Analytics"])
app.include_router(charts.router,       prefix="/admin", tags=["Admin Charts"])
app.include_router(fraud.router,        prefix="/admin", tags=["Fraud Reports"])
app.include_router(auditlog.router,     prefix="/admin", tags=["Audit Logs"])
app.include_router(dealcontrol.router,  prefix="/admin", tags=["Pending Deals"])
app.include_router(usercontrol.router,  prefix="/admin", tags=["User Controls"])
app.include_router(secure_admin.router, prefix="/admin", tags=["Admin Secure"])  # ✅ Verified

# === Future Ready ===
# from routers import notifications, subscriptions
# app.include_router(notifications.router, prefix="/admin", tags=["Notifications"])
