from fastapi import APIRouter

def include_all_routes():
    router = APIRouter()  # ✅ Define router inside function

    from app.api.routes import (
        auth, wallet, deals, disputes, kyc, upload, notifications
    )
    from app.api.routes.admin import (
        analytics, charts, fraud, auditlog, dealcontrol, usercontrol
    )

    router.include_router(auth.router, prefix="/auth")
    router.include_router(wallet.router, prefix="/wallet")
    router.include_router(deals.router, prefix="/deals")
    router.include_router(disputes.router, prefix="/disputes")
    router.include_router(kyc.router, prefix="/kyc")
    router.include_router(upload.router, prefix="/files")
    router.include_router(notifications.router, prefix="/notifications")

    router.include_router(analytics.router, prefix="/admin")
    router.include_router(charts.router, prefix="/admin")
    router.include_router(fraud.router, prefix="/admin")
    router.include_router(auditlog.router, prefix="/admin")
    router.include_router(dealcontrol.router, prefix="/admin")
    router.include_router(usercontrol.router, prefix="/admin")

    return router

__all__ = ["include_all_routes"]
