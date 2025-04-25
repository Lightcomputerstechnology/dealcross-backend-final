from sqlalchemy.orm import Session
from models.fee_transaction import FeeTransaction, FeeType

def log_fee_transaction(db: Session, user_id: int, fee_type: FeeType, amount: float):
    transaction = FeeTransaction(
        user_id=user_id,
        fee_type=fee_type,
        amount=amount
    )
    db.add(transaction)
    db.commit()