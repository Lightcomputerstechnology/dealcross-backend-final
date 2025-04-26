# File: src/app/api/routes/router.py

from fastapi import APIRouter

# Core routers (ensure these files exist)
from . import auth, wallet, deals, disputes, admin, kyc, referrals

# Admin/analytics routers (may trigger errors if missing)
try:
    from . import analytics, metrics, notifications, shares, auditlog, fraud, usercontrol
except ImportError:
    pass  # Skip if module not found

router = APIRouter()

# Include routers (core ones)
router.include_router(auth.router)
router.include_router(wallet.router)
router.include_router(deals.router)
router.include_router(disputes.router)
router.include_router(admin.router)
router.include_router(kyc.router)
router.include_router(referrals.router)

# Include optional routers (admin/analytics)
try:
    router.include_router(analytics.router)
    router.include_router(metrics.router)
    router.include_router(notifications.router)
    router.include_router(shares.router)
    router.include_router(auditlog.router)
    router.include_router(fraud.router)
    router.include_router(usercontrol.router)
except Exception:
    pass  # Skip including if any fails