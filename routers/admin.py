from models.fee_transaction import FeeTransaction  # ✅ Import FeeTransaction
from typing import Optional
from datetime import datetime

# === Admin: View fee transactions ===
@router.get("/fee-transactions", summary="Admin: View all fee transactions")
def view_fee_transactions(
    user_id: Optional[int] = None,
    fee_type: Optional[str] = None,  # 'funding', 'escrow', 'share_buy', 'share_sell'
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Allows admin to view all fee transactions, optionally filtering by:

    - **user_id**: Specific user.
    - **fee_type**: Type of fee ('funding', 'escrow', etc.).
    - **start_date/end_date**: Time range.
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

    return [
        {
            "user_id": tx.user_id,
            "type": tx.type,
            "amount": float(tx.amount),
            "timestamp": tx.timestamp.isoformat()
        } for tx in transactions
    ]
