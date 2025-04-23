from models.fee_transaction import FeeTransaction, FeeType  # ✅ Import Enum

def log_fee_transaction(db, user_id: int, fee_type: FeeType, amount: float):
    """
    Logs a fee transaction using the FeeType enum.

    - fee_type must be one of: FeeType.funding, FeeType.escrow, FeeType.share_buy, FeeType.share_sell
    """
    log = FeeTransaction(
        user_id=user_id,
        type=fee_type,
        amount=amount
    )
    db.add(log)
    db.commit()
