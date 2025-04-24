from fastapi import APIRouter, Depends, HTTPException from sqlalchemy.orm import Session from sqlalchemy import func from core.database import get_db from core.security import get_current_user from models.wallet import Wallet from models.wallet_transaction import WalletTransaction from models.user import User

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions") def get_my_wallet_summary( db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ): """ Returns the current user's wallet balance, transaction summary, and recent transaction history. """ wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first() if not wallet: raise HTTPException(status_code=404, detail={"error": True, "message": "Wallet not found."})

# Wallet summary (funded & spent)
total_funded = db.query(func.sum(WalletTransaction.amount)).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "fund"
).scalar() or 0.00

total_spent = db.query(func.sum(WalletTransaction.amount)).filter(
    WalletTransaction.user_id == current_user.id,
    WalletTransaction.transaction_type == "spend"
).scalar() or 0.00

# Recent 5 transactions
recent_transactions = db.query(WalletTransaction).filter(
    WalletTransaction.user_id == current_user.id
).order_by(WalletTransaction.timestamp.desc()).limit(5).all()

return {
    "message": "Wallet summary retrieved successfully",
    "data": {
        "wallet_balance": float(wallet.balance),
        "summary": {
            "total_funded": total_funded,
            "total_spent": total_spent,
            "net_balance": float(wallet.balance)
        },
        "recent_transactions": [
            {
                "amount": float(tx.amount),
                "type": tx.transaction_type,
                "description": tx.description,
                "timestamp": tx.timestamp.strftime("%B %d, %Y, %I:%M %p")
            } for tx in recent_transactions
        ]
    }
}

