from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.dependencies import get_db, admin_auth_required

router = APIRouter()


@router.get("/admin/analytics")
def get_admin_analytics(db: Session = Depends(get_db), _=Depends(admin_auth_required)):
    # Simulated database counts (replace with real queries)
    total_users = db.query(User).count()
    total_deals = db.query(Deal).count()
    wallets_funded = db.query(WalletTransaction).filter(WalletTransaction.type == "fund").count()
    disputes_raised = db.query(Dispute).count()

    # Simulated fraud alerts
    fraud_alerts = [
        {"type": "Suspicious Login", "count": 6},
        {"type": "VPN Usage", "count": 3},
        {"type": "Unusual Withdrawal", "count": 5}
    ]

    # Simulated API usage stats
    api_metrics = {
        "total_requests": 9832,
        "failed_requests": 147,
        "most_used_endpoints": [
            {"endpoint": "/deals/my-deals", "hits": 2145},
            {"endpoint": "/wallet/balance", "hits": 1976},
            {"endpoint": "/auth/login", "hits": 1823}
        ],
        "last_updated": datetime.utcnow().isoformat()
    }

    return {
        "total_users": total_users,
        "total_deals": total_deals,
        "wallets_funded": wallets_funded,
        "disputes_raised": disputes_raised,
        "fraud_alerts": fraud_alerts,
        "api_metrics": api_metrics
  }
