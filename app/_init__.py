# File: app/api/routes/__init__.py

from fastapi import APIRouter
from routers import auth, wallet, deals, disputes, kyc, upload
# Notification router removed

router = APIRouter()

router.include_router(auth.router)
router.include_router(wallet.router)
router.include_router(deals.router)
router.include_router(disputes.router)
router.include_router(kyc.router)
router.include_router(upload.router)
# router.include_router(notifications.router)  # Temporarily removed