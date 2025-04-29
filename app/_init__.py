# File: app/api/routes/__init__.py

from fastapi import APIRouter
from routers import auth, wallet, deals, disputes, kyc, upload  # ✅ Import active routers only

router = APIRouter()

# Register all available routes
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(wallet.router, prefix="/wallet", tags=["Wallet Management"])
router.include_router(deals.router, prefix="/deals", tags=["Deals"])
router.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
router.include_router(kyc.router, prefix="/kyc", tags=["KYC"])
router.include_router(upload.router, prefix="/upload", tags=["Uploads"])

# router.include_router(notifications.router)  # 🚫 Commented: Notifications disabled for now
