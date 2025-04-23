# File: app/api/routes/__init__.py
from fastapi import APIRouter

router = APIRouter()

# — public
from routers import auth, wallet, deals, disputes, kyc, upload, notifications
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
# …etc for deals, disputes, kyc, upload, notifications…

# — admin
from app.api.routes.admin import analytics, charts, fraud, auditlog, dealcontrol, usercontrol
router.include_router(analytics.router, prefix="/admin/analytics", tags=["Admin Analytics"])
router.include_router(charts.router,    prefix="/admin/charts",    tags=["Admin Charts"])
# …etc for fraud, auditlog, dealcontrol, usercontrol…

__all__ = ["router"]
