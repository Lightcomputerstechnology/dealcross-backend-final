# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from core.dependencies import require_admin
from models.deal import Deal, DealStatus
from models.user import User
from models.audit import AuditLog
from schemas.deal import DealCreate, DealOut
from utils.deal_status import is_valid_transition
from utils.fraud_detection import basic_fraud_check

router = APIRouter(prefix="/deals", tags=["Deals Management"])  # ✅ Tag added

# === Create a new deal ===
@router.post("/create", response_model=DealOut, summary="Create a new deal between users")
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a deal with another user. The deal must have a unique title between the two users
    and must not already be active or pending.

    - **counterparty_id**: The user you're creating the deal with.
    - **title**: The title or name of the deal.
    - **amount**: Deal amount in currency.
    - **description**: Optional description.
    - **public_deal**: If true, this deal is publicly visible.
    """
    counterparty = db.query(User).filter(User.id == payload.counterparty_id).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

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
        db.add(AuditLog(
            admin_id=None,
            action="DEAL AUTO-FLAGGED (FRAUD RULE)",
            target_type="DEAL",
            target_id=new_deal.id
        ))

    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal

# === Get current user's deals ===
@router.get("/tracker", response_model=List[DealOut], summary="Get all your active and past deals")
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all deals involving the current user, whether they are the creator or counterparty.
    """
    deals = db.query(Deal).filter(
        (Deal.creator_id == current_user.id) |
        (Deal.counterparty_id == current_user.id)
    ).all()
    return deals

# === Get public deals ===
@router.get("/public", response_model=List[DealOut], summary="Get all publicly visible deals")
def get_public_deals(db: Session = Depends(get_db)):
    """
    Returns a list of deals that were marked as public and are visible to all users.
    """
    return db.query(Deal).filter(Deal.public_deal == True).all()

# === Update deal status with transition control ===
@router.put("/update-status/{deal_id}", summary="Change the status of a deal")
def update_deal_status(
    deal_id: int,
    new_status: DealStatus,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Updates the status of a deal (e.g., from pending → active, or active → completed/disputed).

    Only the creator, counterparty, or an admin can change the status.
    Invalid transitions will raise an error.
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found.")

    if (current_user.id != deal.creator_id 
        and current_user.id != deal.counterparty_id 
        and not current_user.role == "admin"):
        raise HTTPException(status_code=403, detail="Access denied.")

    if not is_valid_transition(deal.status, new_status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {deal.status} to {new_status}."
        )

    deal.status = new_status
    db.commit()
    db.refresh(deal)
    return {"message": f"Deal status updated to {new_status}.", "deal_id": deal.id}

# === Admin manually flag/unflag deal ===
@router.put("/flag/{deal_id}", summary="Admin: Flag or unflag a deal for fraud")
def flag_deal(
    deal_id: int,
    flag: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Flags or unflags a deal manually (e.g., for fraud alert).

    Only accessible to admin users.
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found.")

    deal.is_flagged = flag
    db.commit()

    db.add(AuditLog(
        admin_id=admin.id,
        action=f"DEAL {'FLAGGED' if flag else 'UNFLAGGED'} (MANUAL)",
        target_type="DEAL",
        target_id=deal.id
    ))
    db.commit()

    return {"message": f"Deal {'flagged' if flag else 'unflagged'} successfully."}
