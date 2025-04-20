# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin

# NEW: Advanced routers
from app.api.routes import analytics, charts, fraud, auditlog, dealcontrol, usercontrol

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="Dealcross Backend", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public Routes
app.include_router(auth.router,       prefix="/auth",     tags=["Authentication"])
app.include_router(wallet.router,     prefix="/wallet",   tags=["Wallet"])
app.include_router(deals.router,      prefix="/deals",    tags=["Deals"])
app.include_router(disputes.router,   prefix="/disputes", tags=["Disputes"])

# Admin & Internal
app.include_router(admin.router,        prefix="/admin", tags=["Admin Core"])
app.include_router(analytics.router,    prefix="/admin", tags=["Admin Analytics"])
app.include_router(charts.router,       prefix="/admin", tags=["Admin Charts"])
app.include_router(fraud.router,        prefix="/admin", tags=["Fraud Reports"])
app.include_router(auditlog.router,     prefix="/admin", tags=["Audit Logs"])
app.include_router(dealcontrol.router,  prefix="/admin", tags=["Pending Deals"])
app.include_router(usercontrol.router,  prefix="/admin", tags=["User Controls"])
