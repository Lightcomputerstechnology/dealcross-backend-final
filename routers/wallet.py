from utils.fee_calculator import calculate_funding_fee
from utils.admin_wallet import credit_admin_wallet
from utils.fee_logger import log_fee_transaction
from models.fee_transaction import FeeType
from sqlalchemy import func

@router.post("/fund", summary="Fund the user's wallet")
def fund_wallet(payload: WalletCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Adds funds to the logged-in user's wallet.

    - Fee deducted based on user tier (2% basic, 1.5% pro).
    - Logs wallet and fee transactions.
    - Returns funding summary.
    """
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid funding amount."})

    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0.00)
        db.add(wallet)

    # Calculate fee
    fee = calculate_funding_fee(payload.amount, current_user.role.value)
    fee_rate = "2%" if current_user.role.value == "basic" else "1.5%"
    net_amount = payload.amount - fee

    # Credit admin wallet
    credit_admin_wallet(db, fee)

    # Log fee transaction
    log_fee_transaction(db, current_user.id, FeeType.funding, fee)

    # Credit user wallet
    wallet.balance += net_amount

    # Log wallet transaction
    db.add(WalletTransaction(
        user_id=current_user.id,
        amount=net_amount,
        transaction_type="fund",
        description="Wallet funded after fee deduction"
    ))

    db.commit()
    db.refresh(wallet)

    # Funding summary
    total_funded = db.query(func.sum(WalletTransaction.amount)).filter(
        WalletTransaction.user_id == current_user.id,
        WalletTransaction.transaction_type == "fund"
    ).scalar() or 0.00

    total_fees_paid = db.query(func.sum(FeeTransaction.amount)).filter(
        FeeTransaction.user_id == current_user.id,
        FeeTransaction.type == FeeType.funding
    ).scalar() or 0.00

    return {
        "message": "Wallet funded successfully",
        "data": {
            "original_amount": payload.amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "user_tier": current_user.role.value,
            "net_amount": net_amount,
            "wallet_balance": float(wallet.balance),
            "funding_summary": {
                "total_funded": total_funded,
                "total_fees_paid": total_fees_paid
            }
        }
    }
