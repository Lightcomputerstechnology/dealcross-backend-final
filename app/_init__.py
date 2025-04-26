# File: app/api/routes/__init__.py

from fastapi import APIRouter
from routers import auth, wallet, deals, disputes, kyc, upload

# Safe import for notifications router
try:
    from routers import notifications
except ImportError:
    notifications = None  # Skip if missing or broken

router = APIRouter()

# Include routers
router.include_router(auth.router)
router.include_router(wallet.router)
router.include_router(deals.router)
router.include_router(disputes.router)
router.include_router(kyc.router)
router.include_router(upload.router)

if notifications:  # Only include if notifications router exists
    router.include_router(notifications.router)