# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.database import Base, engine
from core.middleware import RateLimitMiddleware

# ——————————————————————————————————————————————
# Public API routers (live in your top-level `routers/` folder)
# ——————————————————————————————————————————————
from routers import (
    auth,
    wallet,
    deals,
    disputes,
    kyc,
    upload,
    notifications,
)

# ——————————————————————————————————————————————
# Admin API routers (live in app/api/routes/admin/)
# ——————————————————————————————————————————————
from app.api.routes.admin import (
    analytics,
    charts,
    fraud,
    auditlog,
    dealcontrol,
    usercontrol,
)

# Optional extra-secure admin endpoints
from routers import secure_admin

# ——————————————————————————————————————————————
# Initialize DB (and run your Alembic pre-deploy separately)
# ——————————————————————————————————————————————
Base.metadata.create_all(bind=engine)

# ——————————————————————————————————————————————
# Create the FastAPI app
# ——————————————————————————————————————————————
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description=(
        "FastAPI backend powering the Dealcross platform "
        "with escrow, analytics, fraud detection, admin controls, and more."
    ),
)

# ——————————————————————————————————————————————
# Middleware
# ——————————————————————————————————————————————
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ——————————————————————————————————————————————
# Public routes
# ——————————————————————————————————————————————
app.include_router(auth.router,          prefix="/auth",          tags=["Authentication"])
app.include_router(wallet.router,        prefix="/wallet",        tags=["Wallet Management"])
app.include_router(deals.router,         prefix="/deals",         tags=["Deals Management"])
app.include_router(disputes.router,      prefix="/disputes",      tags=["Dispute Management"])
app.include_router(kyc.router,           prefix="/kyc",           tags=["KYC Verification"])
app.include_router(upload.router,        prefix="/files",         tags=["File Uploads"])
app.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notifications"],
)

# ——————————————————————————————————————————————
# Admin routes
# ——————————————————————————————————————————————
app.include_router(
    analytics.router,
    prefix="/admin/analytics",
    tags=["Admin Analytics"],
)
app.include_router(
    charts.router,
    prefix="/admin/charts",
    tags=["Admin Charts"],
)
app.include_router(
    fraud.router,
    prefix="/admin/fraud",
    tags=["Fraud Reports"],
)
app.include_router(
    auditlog.router,
    prefix="/admin/auditlog",
    tags=["Audit Logs"],
)
app.include_router(
    dealcontrol.router,
    prefix="/admin/deals",
    tags=["Pending Deals"],
)
app.include_router(
    usercontrol.router,
    prefix="/admin/users",
    tags=["User Controls"],
)
# any extra-secure admin endpoints
app.include_router(
    secure_admin.router,
    prefix="/admin/secure",
    tags=["Admin Secure"],
)

# ——————————————————————————————————————————————
# Global exception handlers
# ——————————————————————————————————————————————
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
        content={
            "error": True,
            "code": 400,
            "message": "Validation error",
            "details": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": True, "code": 500, "message": "Internal server error"},
)
