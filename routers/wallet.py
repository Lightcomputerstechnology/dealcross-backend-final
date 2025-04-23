from utils.fee_calculator import calculate_funding_fee
from utils.admin_wallet import credit_admin_wallet
from utils.fee_logger import log_fee_transaction

# === Fund wallet with fee deduction and transaction logging ===
@router.post("/fund", response_model=WalletOut, summary="Fund the user's wallet")
def fund_wallet(payload: WalletCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Adds funds to the logged-in user's wallet.

    - **amount**: The amount to fund the wallet with.
    - **Fee**: Deducted based on user tier (2% basic, 1.5% pro).
    - **Logs**: Wallet and fee transactions recorded.
    """
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0.00)
        db.add(wallet)

    # ✅ Calculate funding fee
    fee = calculate_funding_fee(payload.amount, current_user.role.value)
    net_amount = payload.amount - fee

    # ✅ Credit admin wallet
    credit_admin_wallet(db, fee)

    # ✅ Log fee transaction
    log_fee_transaction(db, current_user.id, "funding", fee)

    # ✅ Credit net amount to user wallet
    wallet.balance += net_amount

    # ✅ Log wallet transaction
    db.add(WalletTransaction(
        user_id=current_user.id,
        amount=net_amount,
        transaction_type="fund",
        description="Wallet funded after fee deduction"
    ))

    db.commit()
    db.refresh(wallet)
    return wallet
