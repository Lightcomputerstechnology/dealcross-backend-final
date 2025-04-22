# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from core.dependencies import require_admin  # ✅ For admin checks
from models.deal import Deal, DealStatus
from models.user import User
from models.audit import AuditLog  # ✅ For audit logs
from schemas.deal import DealCreate, DealOut
from utils.deal_status import is_valid_transition
from utils.fraud_detection import basic_fraud_check  # ✅ For auto-fraud detection

router = APIRouter()

# === Create a new deal ===
@router.post("/create", response_model=DealOut)
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if counterparty exists
    counterparty = db.query(User).filter(User.id == payload.counterparty_id).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

    # Check for duplicate deal
    existing_deal = db.query(Deal).filter(
        Deal.creator_id == current_user.id,
        Deal.counterparty_id == payload.counterparty_id,
        Deal.title == payload.title,
        Deal.status.in_([DealStatus.pending, DealStatus.active])
    ).first()

    if existing_deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A similar deal is already in progress with this counterparty."
        )

    # Create new deal
    new_deal = Deal(
        title=payload.title,
        amount=payload.amount,
        description=payload.description,
        public_deal=payload.public_deal,
        creator_id=current_user.id,
        counterparty_id=payload.counterparty_id
    )

    # Auto-fraud detection
    if basic_fraud_check(new_deal):
        new_deal.is_flagged = True
        # Log auto-fraud detection
        db.add(AuditLog(
            admin_id=None,  # Automated process
            action="DEAL AUTO-FLAGGED (FRAUD RULE)",
            target_type="DEAL",
            target_id=new_deal.id
        ))

    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)

    return new_deal

# === Get current user's deals ===
@router.get("/tracker", response_model=List[DealOut])
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deals = db.query(Deal).filter(
        (Deal.creator_id == current_user.id) |
        (Deal.counterparty_id == current_user.id)
    ).all()
    return deals

# === Get public deals ===
@router.get("/public", response_model=List[DealOut])
def get_public_deals(db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.public_deal == True).all()

# === Update deal status with transition control ===
@router.put("/update-status/{deal_id}")
def update_deal_status(
    deal_id: int,
    new_status: DealStatus,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found.")

    # Only creator, counterparty, or admin can update
    if (current_user.id != deal.creator_id 
        and current_user.id != deal.counterparty_id 
        and not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Access denied.")

    # Validate status transition
    if not is_valid_transition(deal.status, new_status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {deal.status} to {new_status}."
        )

    # Update deal status
    deal.status = new_status
    db.commit()
    db.refresh(deal)

    return {"message": f"Deal status updated to {new_status}.", "deal_id": deal.id}

# === Admin manually flag/unflag deal ===
@router.put("/flag/{deal_id}")
def flag_deal(
    deal_id: int,
    flag: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found.")

    deal.is_flagged = flag
    db.commit()

    # Log manual flagging
    db.add(AuditLog(
        admin_id=admin.id,
        action=f"DEAL {'FLAGGED' if flag else 'UNFLAGGED'} (MANUAL)",
        target_type="DEAL",
        target_id=deal.id
    ))
    db.commit()

    return {"message": f"Deal {'flagged' if flag else 'unflagged'} successfully."}
