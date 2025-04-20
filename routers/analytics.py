# File: routers/analytics.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.deal import Deal
from models.wallet import Wallet
from models.dispute import Dispute

router = APIRouter()

@router.get("/metrics", tags=["Admin"])
def get_admin_metrics(db: Session = Depends(get_db)):
    try:
        total_users = db.query(User).count()
        total_deals = db.query(Deal).count()
        total_funded = db.query(Wallet).filter(Wallet.balance > 0).count()
        total_disputes = db.query(Dispute).count()
        flagged_fraud = db.query(Deal).filter(Deal.fraud_flag == True).count()

        return {
            "users": total_users,
            "deals": total_deals,
            "wallets_funded": total_funded,
            "disputes": total_disputes,
            "fraud_alerts": flagged_fraud
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
