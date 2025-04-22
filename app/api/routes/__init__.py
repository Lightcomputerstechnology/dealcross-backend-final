# File: app/api/routes/__init__.py

from fastapi import APIRouter

def include_all_routes():
    from app.api.routes import auth, wallet, deals, disputes, kyc, upload, notifications
    from app.api.routes.admin import analytics, charts, fraud, auditlog, dealcontrol, usercontrol

    routes = [
        auth.router,
        wallet.router,
        deals.router,
        disputes.router,
        kyc.router,
        upload.router,
        notifications.router,
        analytics.router,
        charts.router,
        fraud.router,
        auditlog.router,
        dealcontrol.router,
        usercontrol.router,
    ]
    return routes

__all__ = ["include_all_routes"]
