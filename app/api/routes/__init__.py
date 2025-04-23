# File: app/api/routes/__init__.py

from fastapi import APIRouter

router = APIRouter()

def include_all_routes():
    # Import inside function to avoid circular imports
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

    # Include routers
    router.include_router(auth.router)
    router.include_router(wallet.router)
    router.include_router(deals.router)
    router.include_router(disputes.router)
    router.include_router(kyc.router)
    router.include_router(upload.router)
    router.include_router(notifications.router)

    router.include_router(analytics.router)
    router.include_router(charts.router)
    router.include_router(fraud.router)
    router.include_router(auditlog.router)
    router.include_router(dealcontrol.router)
    router.include_router(usercontrol.router)

    return router

__all__ = ["include_all_routes"]
