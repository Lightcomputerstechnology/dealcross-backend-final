# File: main.py

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.database import Base, engine
from core.middleware import RateLimitMiddleware

# — Public API routers (live in your top-level routers/ folder)
from routers.auth import router as auth_router
from routers.wallet import router as wallet_router
from routers.deals import router as deals_router
from routers.disputes import router as disputes_router
from routers.kyc import router as kyc_router
from routers.upload import router as upload_router
from routers.notifications import router as notifications_router

# — Admin API routers (live in app/api/routes/admin/)
from app.api.routes.admin.analytics import router as analytics_router
from app.api.routes.admin.charts    import router as charts_router
from app.api.routes.admin.fraud     import router as fraud_router
from app.api.routes.admin.auditlog  import router as auditlog_router
from app.api.routes.admin.dealcontrol  import router as dealcontrol_router
from app.api.routes.admin.usercontrol  import router as usercontrol_router

# — (Optional) extra-secure admin endpoints
from routers.secure_admin import router as secure_admin_router

# — Create all tables (run your Alembic pre-deploy separately)
Base.metadata.create_all(bind=engine)

# — FastAPI instantiation
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description=(
        "FastAPI backend powering the Dealcross platform "
        "with escrow, analytics, fraud detection, admin controls, and more."
    ),
)

# — Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_ORIGINS", "*").split(","),  # lock this down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# — Public API routes
app.include_router(auth_router,          prefix="/auth",        tags=["Authentication"])
app.include_router(wallet_router,        prefix="/wallet",      tags=["Wallet Management"])
app.include_router(deals_router,         prefix="/deals",       tags=["Deals Management"])
app.include_router(disputes_router,      prefix="/disputes",    tags=["Dispute Management"])
app.include_router(kyc_router,           prefix="/kyc",         tags=["KYC Verification"])
app.include_router(upload_router,        prefix="/files",       tags=["File Uploads"])
app.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])

# — Admin API routes
app.include_router(analytics_router,   prefix="/admin/analytics", tags=["Admin Analytics"])
app.include_router(charts_router,      prefix="/admin/charts",    tags=["Admin Charts"])
app.include_router(fraud_router,       prefix="/admin/fraud",     tags=["Fraud Reports"])
app.include_router(auditlog_router,    prefix="/admin/auditlog",  tags=["Audit Logs"])
app.include_router(dealcontrol_router, prefix="/admin/deals",     tags=["Pending Deals"])
app.include_router(usercontrol_router, prefix="/admin/users",     tags=["User Controls"])
app.include_router(secure_admin_router, prefix="/admin/secure",    tags=["Admin Secure"])

# — Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "code": exc.status_code, "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": True, "code": 400, "message": "Validation error", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # you can log `exc` here if you want
    return JSONResponse(
        status_code=500,
        content={"error": True, "code": 500, "message": "Internal server error"},
)
