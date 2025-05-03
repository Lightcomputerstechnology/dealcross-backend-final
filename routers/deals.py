# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException
from decimal import Decimal
from core.security import get_current_user
from models.deal import Deal
from models.user import User
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from schemas.deal import DealCreate, DealOut
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarning
from services.fee_logic import calculate_fee

router = APIRouter(prefix="/deals", tags=["Deals"])

# ─────────── CREATE DEAL ───────────
@router.post("/", response_model=DealOut, summary="Create a new deal")
async def create_deal(
    deal: DealCreate,
    current_user: User = Depends(get_current_user),
) -> DealOut:
    new_deal = await Deal.create(
        **deal.dict(),
        creator=current_user,
        status="pending"
    )
    return DealOut.model_validate(new_deal)

# ─────────── GET PENDING PAIRINGS ───────────
@router.get("/pairing/pending", summary="Fetch pending pairings for user")
async def get_pending_pairings(current_user: User = Depends(get_current_user)):
    pairings = await Deal.filter(counterparty=None).exclude(creator=current_user)
    return [DealOut.model_validate(p) for p in pairings]

# ─────────── CONFIRM PAIRING ───────────
@router.post("/pairing/confirm/{deal_id}", summary="Confirm and pair a deal")
async def confirm_pairing(
    deal_id: int,
    current_user: User = Depends(get_current_user)
):
    deal = await Deal.get_or_none(id=deal_id, counterparty=None)
    if not deal or deal.creator_id == current_user.id:
        raise HTTPException(status_code=400, detail="Invalid deal for pairing.")

    deal.counterparty = current_user
    deal.status = "paired"
    await deal.save()

    return {"message": "Pairing confirmed."}

# ─────────── FUND DEAL (UPDATED) ───────────
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

    wallet.balance -= total_deduction
    await wallet.save()

    deal.status = "active"
    deal.escrow_locked = base_amount  # Requires field in model
    await deal.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=base_amount,
        transaction_type="escrow_fund",
        description=f"Funded Deal {deal.id} (fee: {fee})"
    )

    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)
    admin_wallet.balance += fee
    await admin_wallet.save()

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

# ─────────── MARK DEAL AS DELIVERED ───────────
@router.post("/{deal_id}/deliver", summary="Mark a deal as delivered")
async def mark_delivered(
    deal_id: int,
    current_user: User = Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id, counterparty=current_user)
    if not deal or deal.status != "active":
        raise HTTPException(status_code=400, detail="Deal not found or cannot be marked delivered.")

    deal.status = "completed"
    await deal.save()

    return {"message": "Deal marked as delivered."}

# ─────────── RELEASE FUNDS ───────────
@router.post("/{deal_id}/release", summary="Release funds for a completed deal")
async def release_funds(
    deal_id: int,
    current_user: User = Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id, creator=current_user)
    if not deal or deal.status != "completed":
        raise HTTPException(status_code=400, detail="Deal not ready for release.")

    seller_wallet = await Wallet.get(user=deal.counterparty)
    seller_wallet.balance += deal.escrow_locked
    await seller_wallet.save()

    await WalletTransaction.create(
        wallet=seller_wallet,
        user=deal.counterparty,
        amount=deal.escrow_locked,
        transaction_type="escrow_release",
        description=f"Released funds for Deal {deal.id}"
    )

    return {"message": "Funds released to seller."}

# ─────────── RAISE DISPUTE ───────────
@router.post("/{deal_id}/dispute", summary="Raise a dispute on a deal")
async def raise_dispute(
    deal_id: int,
    current_user: User = Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id)
    if (
        not deal or
        (deal.creator_id != current_user.id and deal.counterparty_id != current_user.id) or
        deal.status not in ["active", "completed"]
    ):
        raise HTTPException(status_code=400, detail="Cannot dispute this deal.")

    deal.status = "disputed"
    await deal.save()

    return {"message": "Deal marked as disputed."}
    
