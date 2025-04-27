from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.pairing import Pairing, PairingStatus
from models import User
from schemas.pairing import PairRequest, PairOut

router = APIRouter(prefix="/deals", tags=["Deal Pairing"])

# Initiate Pairing
@router.post("/pair", response_model=PairOut)
def initiate_pairing(
    payload: PairRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find counterparty
    counterparty = db.query(User).filter(User.email == payload.counterparty_email).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found.")

    # Prevent self-pairing
    if counterparty.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot pair with yourself.")

    # Check if pairing exists
    existing = db.query(Pairing).filter(
        Pairing.creator_id == current_user.id,
        Pairing.counterparty_id == counterparty.id,
        Pairing.status == PairingStatus.pending
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Pairing already pending.")

    # Create pairing
    new_pair = Pairing(creator_id=current_user.id, counterparty_id=counterparty.id)
    db.add(new_pair)
    db.commit()
    db.refresh(new_pair)
    return new_pair

# Confirm Pairing
@router.post("/pair/{pair_id}/confirm", response_model=PairOut)
def confirm_pairing(
    pair_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pairing = db.query(Pairing).filter(Pairing.id == pair_id).first()
    if not pairing:
        raise HTTPException(status_code=404, detail="Pairing not found.")

    # Only counterparty can confirm
    if pairing.counterparty_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to confirm this pairing.")

    if pairing.status != PairingStatus.pending:
        raise HTTPException(status_code=400, detail="Pairing already processed.")

    pairing.status = PairingStatus.confirmed
    db.commit()
    db.refresh(pairing)
    return pairing