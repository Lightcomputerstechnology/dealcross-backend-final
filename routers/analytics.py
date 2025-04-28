Analytics Metrics (Tortoise ORM Version)

from fastapi import APIRouter, Depends from core.dependencies import require_admin  # ✅ Admin check from models.user import User from models.deal import Deal from models.wallet import Wallet from models.dispute import Dispute

router = APIRouter()

@router.get("/metrics", tags=["Admin"]) async def get_admin_metrics(admin=Depends(require_admin)):  # ✅ Protect route total_users = await User.all().count() total_deals = await Deal.all().count() total_funded = await Wallet.filter(balance__gt=0).count() total_disputes = await Dispute.all().count() flagged_fraud = await Deal.filter(is_flagged=True).count()  # ✅ Updated field

return {
    "users": total_users,
    "deals": total_deals,
    "wallets_funded": total_funded,
    "disputes": total_disputes,
    "fraud_alerts": flagged_fraud
}

