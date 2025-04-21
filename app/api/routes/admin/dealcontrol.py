from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.deal import Deal

router = APIRouter()


@router.get("/pending-deals")
def get_pending_deals(db: Session = Depends(get_db)):
    pending = db.query(Deal).filter(Deal.status == "Pending").all()
    return [
        {
            "id": d.id,
            "title": d.title,
            "amount": d.amount,
            "status": d.status,
            "public_deal": d.public_deal,
            "counterparty_email": d.counterparty_email,
            "created_at": d.created_at.strftime("%Y-%m-%d"),
        }
        for d in pending
    ]


@router.post("/approve-deal/{deal_id}")
def approve_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    approval_note: Optional[str] = Body(None, embed=True)
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "Approved"
    if approval_note:
        deal.approval_note = approval_note
    db.commit()
    return {"message": f"Deal {deal_id} approved successfully."}


@router.post("/reject-deal/{deal_id}")
def reject_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    reason: Optional[str] = Body(None, embed=True)
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "Rejected"
    if reason:
        deal.rejection_reason = reason  # You can create this field in models if needed
    db.commit()
    return {"message": f"Deal {deal_id} rejected."}
