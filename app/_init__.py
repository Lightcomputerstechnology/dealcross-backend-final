from fastapi import APIRouter
from routers import auth, wallet, deals, disputes, kyc, upload  # ✅ Removed notifications

router = APIRouter()

# Include routes
router.include_router(auth.router)
router.include_router(wallet.router)
router.include_router(deals.router)
router.include_router(disputes.router)
router.include_router(kyc.router)
router.include_router(upload.router)
# router.include_router(notifications.router)  # Commented out notifications