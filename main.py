# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.database import Base, engine
from core.middleware import RateLimitMiddleware

# === Import All Routers Directly ===
from app.api.routes import (
    auth,
    wallet,
    deals,
    disputes,
    kyc,
    upload,
    notifications
)
from app.api.routes.admin import (
    analytics,
    charts,
    fraud,
    auditlog,
    dealcontrol,
    usercontrol
)
from routers import secure_admin  # ✅ Extra admin protection

# === Initialize Database ===
Base.metadata.create_all(bind=engine)

# === Initialize FastAPI App ===
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend powering the Dealcross platform with escrow, analytics, fraud detection, admin controls, and more.",
)

# === Middleware ===
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain before production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Public API Routes ===
app.include_router(auth.router,           prefix="/auth",           tags=["Authentication"])
app.include_router(wallet.router,         prefix="/wallet",         tags=["Wallet Management"])
app.include_router(deals.router,          prefix="/deals",          tags=["Deals Management"])
app.include_router(disputes.router,       prefix="/disputes",       tags=["Dispute Management"])
app.include_router(kyc.router,            prefix="/kyc",            tags=["KYC Verification"])
app.include_router(upload.router,         prefix="/files",          tags=["File Uploads"])
app.include_router(notifications.router,  prefix="/notifications",  tags=["Notifications"])

# === Admin API Routes ===
app.include_router(analytics.router,      prefix="/admin",          tags=["Admin Analytics"])
app.include_router(charts.router,         prefix="/admin",          tags=["Admin Charts"])
app.include_router(fraud.router,          prefix="/admin",          tags=["Fraud Reports"])
app.include_router(auditlog.router,       prefix="/admin",          tags=["Audit Logs"])
app.include_router(dealcontrol.router,    prefix="/admin",          tags=["Pending Deals"])
app.include_router(usercontrol.router,    prefix="/admin",          tags=["User Controls"])
app.include_router(secure_admin.router,   prefix="/admin",          tags=["Admin Secure"])

# === Global Exception Handling ===
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "code": exc.status_code, "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": True, "code": 400, "message": "Validation error", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": True, "code": 500, "message": "Internal server error"},
)
