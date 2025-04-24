from fastapi import APIRouter, Depends, HTTPException from sqlalchemy.orm import Session from sqlalchemy import func from datetime import datetime, timedelta

from core.database import get_db from core.security import get_current_user from models.wallet import Wallet from models.wallet_transaction import WalletTransaction from models.user import User from models.fee_transaction import FeeTransaction from models.fraud_alert import FraudAlert  # ✅ Added for fraud alerts

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

=== Fraud alert utility ===

def trigger_fraud_alert(db: Session, user_id: int, alert_type: str, description: str): alert = FraudAlert( user_id=user_id, alert_type=alert_type, description=description ) db.add(alert) db.commit()

@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions") def get_my_wallet_summary( db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ): wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first() if not wallet: raise HTTPException(status_code=404, detail={"error": True, "message": "Wallet not found."})

# Wallet summary
total_funded = db.query(func.sum(WalletTransaction.amount)).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "fund"
).scalar() or 0.00

total_spent = db.query(func.sum(WalletTransaction.amount)).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "spend"
).scalar() or 0.00

total_fees_paid = db.query(func.sum(FeeTransaction.amount)).filter(
    FeeTransaction.user_id == current_user.id
).scalar() or 0.00

total_transactions = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id
).count()

funds_added_count = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "fund"
).count()

spends_count = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "spend"
).count()

recent_transactions = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id
).order_by(WalletTransaction.timestamp.desc()).limit(5).all()

def relative_time(timestamp):
    delta = datetime.utcnow() - timestamp
    if delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.seconds > 3600:
        return f"{delta.seconds // 3600} hours ago"
    elif delta.seconds > 60:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return "Just now"

# === Fraud detection: frequent funding ===
ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
recent_fundings = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "fund",
    WalletTransaction.timestamp >= ten_minutes_ago
).count()

if recent_fundings >= 5:
    trigger_fraud_alert(db, current_user.id, "frequent_funding", f"User funded wallet {recent_fundings} times within 10 minutes.")

return {
    "message": "Wallet summary retrieved successfully",
    "data": {
        "wallet_balance": float(wallet.balance),
        "currency": "USD",
        "summary": {
            "total_funded": total_funded,
            "total_spent": total_spent,
            "total_fees_paid": total_fees_paid,
            "net_balance": float(wallet.balance),
            "total_transactions": total_transactions,
            "transaction_breakdown": {
                "funds_added": funds_added_count,
                "spends": spends_count
            }
        },
        "recent_transactions": [
            {
                "amount": float(tx.amount),
                "type": tx.transaction_type,
                "description": tx.description,
                "timestamp": tx.timestamp.strftime("%B %d, %Y, %I:%M %p"),
                "relative_time": relative_time(tx.timestamp)
            } for tx in recent_transactions
        ]
    }
}

