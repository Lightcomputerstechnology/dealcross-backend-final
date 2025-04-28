Deal Pairing Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException, status from core.security import get_current_user from models.pairing import Pairing, PairingStatus from models.user import User from schemas.pairing import PairRequest, PairOut

router = APIRouter(prefix="/deals", tags=["Deal Pairing"])

Initiate Pairing

@router.post("/pair", response_model=PairOut) async def initiate_pairing( payload: PairRequest, current_user: User = Depends(get_current_user) ): counterparty = await User.get_or_none(email=payload.counterparty_email) if not counterparty: raise HTTPException(status_code=404, detail="Counterparty not found.")

if counterparty.id == current_user.id:
    raise HTTPException(status_code=400, detail="Cannot pair with yourself.")

existing = await Pairing.filter(
    creator=current_user,
    counterparty=counterparty,
    status=PairingStatus.pending
).first()

if existing:
    raise HTTPException(status_code=400, detail="Pairing already pending.")

new_pair = await Pairing.create(
    creator=current_user,
    counterparty=counterparty
)
return new_pair

Confirm Pairing

@router.post("/pair/{pair_id}/confirm", response_model=PairOut) async def confirm_pairing( pair_id: int, current_user: User = Depends(get_current_user) ): pairing = await Pairing.get_or_none(id=pair_id) if not pairing: raise HTTPException(status_code=404, detail="Pairing not found.")

if pairing.counterparty_id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized to confirm this pairing.")

if pairing.status != PairingStatus.pending:
    raise HTTPException(status_code=400, detail="Pairing already processed.")

pairing.status = PairingStatus.confirmed
await pairing.save()
return pairing

