# File: routers/admin_controls.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import User
from models.deal import Deal
from schemas.admin_controls import BlockAction, DealApproval

router = APIRouter()

# GET all users
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Block a user
@router.post("/users/block")
def block_user(data: BlockAction, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_blocked = True
    user.block_reason = data.reason
    db.commit()
    return {"message": "User blocked successfully."}

# Unblock a user
@router.post("/users/unblock")
def unblock_user(data: BlockAction, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_blocked = False
    user.block_reason = None
    db.commit()
    return {"message": "User unblocked successfully."}

# Approve a deal
@router.post("/deals/approve")
def approve_deal(data: DealApproval, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == data.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "approved"
    deal.approval_note = data.note
    db.commit()
    return {"message": "Deal approved."}

# Reject a deal
@router.post("/deals/reject")
def reject_deal(data: DealApproval, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == data.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "rejected"
    deal.approval_note = data.note
    db.commit()
    return {"message": "Deal rejected."}
