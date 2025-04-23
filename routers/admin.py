from models.fee_transaction import FeeTransaction, FeeType
from typing import Optional
from datetime import datetime
from fastapi import Query
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

from sqlalchemy.orm import Session
from fastapi import Depends
from core.database import get_db
from models.user import User
from core.dependencies import require_admin

# === Admin: View fee transactions with total sum ===
@router.get("/fee-transactions", summary="Admin: View all fee transactions")
def view_fee_transactions(
    user_id: Optional[int] = None,
    fee_type: Optional[FeeType] = Query(None),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Allows admin to view all fee transactions with optional filters.
    Includes total fee amount sum.
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

    # Format timestamp and calculate total
    total_amount = sum(float(tx.amount) for tx in transactions)

    formatted_transactions = [
        {
            "user_id": tx.user_id,
            "type": tx.type.value,
            "amount": float(tx.amount),
            "timestamp": tx.timestamp.strftime("%B %d, %Y, %I:%M %p")  # Human-readable
        } for tx in transactions
    ]

    return {
        "total_transactions": len(transactions),
        "total_amount": total_amount,
        "transactions": formatted_transactions
    }

# === Admin: Export fee transactions as CSV ===
@router.get("/fee-transactions/export", summary="Admin: Export fee transactions as CSV")
def export_fee_transactions_csv(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Exports all fee transactions as a CSV file.
    """
    transactions = db.query(FeeTransaction).order_by(FeeTransaction.timestamp.desc()).all()

    def generate():
        data = StringIO()
        writer = csv.writer(data)
        writer.writerow(["User ID", "Fee Type", "Amount", "Timestamp"])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for tx in transactions:
            writer.writerow([tx.user_id, tx.type.value, float(tx.amount), tx.timestamp.strftime("%B %d, %Y, %I:%M %p")])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    return StreamingResponse(generate(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=fee_transactions.csv"})
