# File: app/api/routes/__init__.py
from fastapi import APIRouter

router = APIRouter()

def include_all_routes() -> APIRouter:
    """
    Import & mount every sub-router.  Called by main.py.
    """
    # — public endpoints (in routers/ folder)
    from routers import auth, wallet, deals, disputes, kyc, upload, notifications

    # — admin endpoints (in app/api/routes/admin)
    from .admin import analytics, charts, fraud, auditlog, dealcontrol, usercontrol

    # mount public
    router.include_router(auth.router,        prefix="/auth",     tags=["Authentication"])
    router.include_router(wallet.router,      prefix="/wallet",   tags=["Wallet Management"])
    router.include_router(deals.router,       prefix="/deals",    tags=["Deals Management"])
    router.include_router(disputes.router,    prefix="/disputes", tags=["Dispute Management"])
    router.include_router(kyc.router,         prefix="/kyc",      tags=["KYC Verification"])
    router.include_router(upload.router,      prefix="/files",    tags=["File Uploads"])
    router.include_router(
      notifications.router,
      prefix="/notifications",
      tags=["Notifications"]
    )

    # mount admin
    router.include_router(analytics.router,   prefix="/admin/analytics", tags=["Admin Analytics"])
    router.include_router(charts.router,      prefix="/admin/charts",    tags=["Admin Charts"])
    router.include_router(fraud.router,       prefix="/admin/fraud",     tags=["Fraud Reports"])
    router.include_router(auditlog.router,    prefix="/admin/auditlog",  tags=["Audit Logs"])
    router.include_router(dealcontrol.router, prefix="/admin/deals",     tags=["Pending Deals"])
    router.include_router(usercontrol.router, prefix="/admin/users",     tags=["User Controls"])

    return router
