from models.fee_transaction import FeeTransaction

def log_fee_transaction(db, user_id: int, fee_type: str, amount: float):
    log = FeeTransaction(
        user_id=user_id,
        type=fee_type,  # 'funding', 'escrow', 'share_buy', 'share_sell'
        amount=amount
    )
    db.add(log)
    db.commit()
