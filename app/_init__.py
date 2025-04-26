# File: src/app/api/routes/__init__.py

from fastapi import APIRouter

# Import all routers (whether created or pending creation)
from app.api.routes import (
    auth,
    wallet,
    deals,
    disputes,
    admin,
    kyc,
    referrals,
    analytics,
    metrics,
    notifications,  # Pending creation or confirmation
    shares,          Share trading router
    auditlog,        Admin audit log router
    fraud,           Fraud alerts
    usercontrol      Admin user management
)

# Initialize main API router
router = APIRouter()

# Include routers (adjust prefixes inside individual router files)
router.include_router(auth.router)
router.include_router(wallet.router)
router.include_router(deals.router)
router.include_router(disputes.router)
router.include_router(admin.router)
router.include_router(kyc.router)
router.include_router(referrals.router)
router.include_router(analytics.router)
router.include_router(metrics.router)
router.include_router(notifications.router)
router.include_router(shares.router)
router.include_router(auditlog.router)
router.include_router(fraud.router)
router.include_router(usercontrol.router)
