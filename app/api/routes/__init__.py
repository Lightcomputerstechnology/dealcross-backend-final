# File: app/api/routes/__init__.py

from fastapi import APIRouter

router = APIRouter()

# — public
from routers import auth, wallet, deals, disputes, kyc, upload, notifications

from routers import blog
router.include_router(blog.router, prefix="/blog", tags=["Blog"])

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
router.include_router(deals.router, prefix="/deals", tags=["Deals"])
router.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
router.include_router(kyc.router, prefix="/kyc", tags=["KYC"])
router.include_router(upload.router, prefix="/upload", tags=["Uploads"])
# router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])  # (Optional)

# — admin
from app.api.routes.admin import analytics, charts, fraud, auditlog, dealcontrol, usercontrol

router.include_router(analytics.router, prefix="/admin/analytics", tags=["Admin Analytics"])
router.include_router(charts.router, prefix="/admin/charts", tags=["Admin Charts"])
router.include_router(fraud.router, prefix="/admin/fraud", tags=["Admin Fraud"])
router.include_router(auditlog.router, prefix="/admin/auditlog", tags=["Admin Audit Logs"])
router.include_router(dealcontrol.router, prefix="/admin/dealcontrol", tags=["Admin Deal Control"])
router.include_router(usercontrol.router, prefix="/admin/usercontrol", tags=["Admin User Control"])

# — Home Route
@router.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Dealcross API - Backend is Live!"}

# Export
__all__ = ["router"]
