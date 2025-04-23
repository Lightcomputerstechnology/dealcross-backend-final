# File: app/api/routes/__init__.py

from fastapi import APIRouter

def include_all_routes() -> APIRouter:
    router = APIRouter()

    # Lazy imports inside the function scope to avoid circular imports
    from . import auth, wallet, deals, disputes, kyc, upload, notifications
    from .admin import analytics, charts, fraud, auditlog, dealcontrol, usercontrol

    # Public routes
    router.include_router(auth.router,       prefix="/auth",     tags=["Authentication"])
    router.include_router(wallet.router,     prefix="/wallet",   tags=["Wallet Management"])
    router.include_router(deals.router,      prefix="/deals",    tags=["Deals Management"])
    router.include_router(disputes.router,   prefix="/disputes", tags=["Dispute Management"])
    router.include_router(kyc.router,        prefix="/kyc",      tags=["KYC Verification"])
    router.include_router(upload.router,     prefix="/files",    tags=["File Uploads"])
    router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

    # Admin routes
    router.include_router(analytics.router,    prefix="/admin", tags=["Admin Analytics"])
    router.include_router(charts.router,       prefix="/admin", tags=["Admin Charts"])
    router.include_router(fraud.router,        prefix="/admin", tags=["Fraud Reports"])
    router.include_router(auditlog.router,     prefix="/admin", tags=["Audit Logs"])
    router.include_router(dealcontrol.router,  prefix="/admin", tags=["Pending Deals"])
    router.include_router(usercontrol.router,  prefix="/admin", tags=["User Controls"])

    return router

__all__ = ["include_all_routes"]
