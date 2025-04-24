from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from core.database import get_db
from core.security import get_current_user
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.fee_transaction import FeeTransaction
from models.fraud_alert import FraudAlert
from models.user import User
from schemas.wallet import WalletOut, FundWallet, TransactionOut

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

# ─────────── FRAUD ALERT HELPER ───────────
def trigger_fraud_alert(db: Session, user_id: int, alert_type: str, description: str):
    alert = FraudAlert(user_id=user_id, alert_type=alert_type, description=description)
    db.add(alert)
    db.commit()

# ─────────── GET WALLET SUMMARY ───────────
@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions")
def get_my_wallet_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found.")

    # Summaries
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

    recent_transactions = db.query(WalletTransaction).filter(
        WalletTransaction.user_id == current_user.id
    ).order_by(WalletTransaction.timestamp.desc()).limit(5).all()

    # Fraud Detection: Frequent Funding
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_fundings = db.query(WalletTransaction).filter(
        WalletTransaction.user_id == current_user.id,
        WalletTransaction.transaction_type == "fund",
        WalletTransaction.timestamp >= ten_minutes_ago
    ).count()

    if recent_fundings >= 5:
        trigger_fraud_alert(db, current_user.id, "frequent_funding", f"User funded wallet {recent_fundings} times within 10 minutes.")

    return {
        "wallet": WalletOut.model_validate(wallet),
        "summary": {
            "total_funded": total_funded,
            "total_spent": total_spent,
            "total_fees_paid": total_fees_paid,
        },
        "recent_transactions": [TransactionOut.model_validate(tx) for tx in recent_transactions]
    }

# ─────────── FUND WALLET ───────────
@router.post("/fund", summary="Fund user's wallet")
def fund_wallet(fund: FundWallet, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0.0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

    wallet.balance += fund.amount
    transaction = WalletTransaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        amount=fund.amount,
        transaction_type="fund",
        description="Wallet funding"
    )
    db.add(transaction)
    db.commit()
    return {"message": f"Wallet funded with {fund.amount} USD"}