Deals Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from core.security import get_current_user from models.deal import Deal, DealStatus from models.user import User from models.wallet import Wallet from models.wallettransaction import WalletTransaction from schemas.deal import DealCreate, DealOut

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("/", response_model=DealOut, summary="Create a new deal") async def create_deal( deal: DealCreate, current_user: User = Depends(get_current_user), ) -> DealOut: new_deal = await Deal.create( **deal.dict(), creator=current_user, status=DealStatus.pending ) return new_deal

@router.post("/{deal_id}/fund", summary="Fund a deal") async def fund_deal( deal_id: int, current_user: User = Depends(get_current_user), ): deal = await Deal.get_or_none(id=deal_id, creator=current_user) if not deal or deal.status != DealStatus.pending: raise HTTPException(status_code=400, detail="Deal not found or cannot be funded.")

wallet = await Wallet.get(user=current_user)
if wallet.balance < deal.amount:
    raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

wallet.balance -= deal.amount
await wallet.save()

deal.status = DealStatus.active
await deal.save()

await WalletTransaction.create(
    wallet=wallet,
    user=current_user,
    amount=deal.amount,
    transaction_type="escrow_fund",
    description=f"Funded Deal {deal.id}",
)

return {"message": "Deal funded successfully."}

@router.post("/{deal_id}/deliver", summary="Mark a deal as delivered") async def mark_delivered( deal_id: int, current_user: User = Depends(get_current_user), ): deal = await Deal.get_or_none(id=deal_id, counterparty=current_user) if not deal or deal.status != DealStatus.active: raise HTTPException(status_code=400, detail="Deal not found or cannot be marked delivered.")

deal.status = DealStatus.completed
await deal.save()

return {"message": "Deal marked as delivered."}

@router.post("/{deal_id}/release", summary="Release funds for a completed deal") async def release_funds( deal_id: int, current_user: User = Depends(get_current_user), ): deal = await Deal.get_or_none(id=deal_id, creator=current_user) if not deal or deal.status != DealStatus.completed: raise HTTPException(status_code=400, detail="Deal not ready for release.")

seller_wallet = await Wallet.get(user=deal.counterparty)
seller_wallet.balance += deal.amount
await seller_wallet.save()

await WalletTransaction.create(
    wallet=seller_wallet,
    user=deal.counterparty,
    amount=deal.amount,
    transaction_type="escrow_release",
    description=f"Released funds for Deal {deal.id}",
)

return {"message": "Funds released to seller."}

@router.post("/{deal_id}/dispute", summary="Raise a dispute on a deal") async def raise_dispute( deal_id: int, current_user: User = Depends(get_current_user), ): deal = await Deal.get_or_none(id=deal_id) if not deal or (deal.creator_id != current_user.id and deal.counterparty_id != current_user.id) or deal.status not in [DealStatus.active, DealStatus.completed]: raise HTTPException(status_code=400, detail="Cannot dispute this deal.")

deal.status = DealStatus.disputed
await deal.save()

return {"message": "Deal marked as disputed."}

