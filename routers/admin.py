from models.fee_transaction import FeeTransaction, FeeType
from typing import Optional
from datetime import datetime
from fastapi import Query
from sqlalchemy.orm import Session
from fastapi import Depends
from core.database import get_db
from models.user import User
from core.dependencies import require_admin

# === Admin: View fee transactions with totals ===
@router.get("/fee-transactions", summary="Admin: View all fee transactions with metrics")
def view_fee_transactions(
    user_id: Optional[int] = None,
    fee_type: Optional[FeeType] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Allows admin to view all fee transactions, optionally filtering by:

    - **user_id**: Specific user.
    - **fee_type**: Enum ('funding', 'escrow', 'share_buy', 'share_sell').
    - **start_date/end_date**: Time range.

    Adds transaction count and total amount.
    """
    query = db.query(FeeTransaction)

    if user_id:
        query = query.filter(FeeTransaction.user_id == user_id)
    if fee_type:
        query = query.filter(FeeTransaction.type == fee_type)
    if start_date:
        query = query.filter(FeeTransaction.timestamp >= start_date)
    if end_date:
        query = query.filter(FeeTransaction.timestamp <= end_date)

    transactions = query.order_by(FeeTransaction.timestamp.desc()).all()

    total_amount = sum(float(tx.amount) for tx in transactions)
    count = len(transactions)

    formatted_transactions = [
        {
            "user_id": tx.user_id,
            "type": tx.type.value,
            "amount": float(tx.amount),
            "timestamp": tx.timestamp.strftime("%B %d, %Y, %I:%M %p")  # Human-readable
        } for tx in transactions
    ]

    return {
        "total_transactions": count,
        "total_amount": total_amount,
        "transactions": formatted_transactions
    }
