from decimal import Decimal
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarning
from services.fee_logic import calculate_fee

@router.post("/{deal_id}/fund", summary="Fund a deal (escrow fee applies)")
async def fund_deal(
    deal_id: int,
    current_user: User = Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id, creator=current_user)
    if not deal or deal.status != "paired":
        raise HTTPException(status_code=400, detail="Deal not found or cannot be funded.")

    wallet = await Wallet.get(user=current_user)
    base_amount = Decimal(deal.amount)
    fee = Decimal(calculate_fee(current_user, "escrow", float(base_amount)))
    total_deduction = base_amount + fee

    if wallet.balance < total_deduction:
        raise HTTPException(status_code=400, detail="Insufficient balance (escrow + fee).")

    # 1. Deduct full amount from user wallet
    wallet.balance -= total_deduction
    await wallet.save()

    # 2. Update deal status and lock amount
    deal.status = "active"
    deal.escrow_locked = base_amount   # You must add this field in Deal model
    await deal.save()

    # 3. Log transaction
    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=base_amount,
        transaction_type="escrow_fund",
        description=f"Funded Deal {deal.id} (fee: {fee})"
    )

    # 4. Add fee to admin wallet
    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)
    admin_wallet.balance += fee
    await admin_wallet.save()

    # 5. Log platform earnings
    await PlatformEarning.create(
        user=current_user,
        source="escrow",
        amount=fee
    )

    return {
        "message": f"Deal funded with {base_amount} (fee {fee})",
        "net_funded": float(base_amount),
        "fee": float(fee)
    }
