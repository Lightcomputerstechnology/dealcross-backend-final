# File: src/app/api/routes/admin/dealcontrol.py

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
from models.deal import Deal
from core.security import get_current_user

router = APIRouter(prefix="/admin/dealcontrol", tags=["Admin - Deal Control"])

# === Get pending deals ===
@router.get("/pending-deals")
async def get_pending_deals(current_user=Depends(get_current_user)):
    pending = await Deal.filter(status="pending").all()

    return [
        {
            "id": d.id,
            "title": d.title,
            "amount": float(d.amount),
            "status": d.status,
            "public_deal": d.public_deal,
            "counterparty_email": d.counterparty_email,
            "created_at": d.created_at.strftime("%Y-%m-%d"),
        }
        for d in pending
    ]

# === Approve a deal ===
@router.post("/approve-deal/{deal_id}")
async def approve_deal(
    deal_id: int,
    approval_note: Optional[str] = Body(None, embed=True),
    current_user=Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.status = "approved"
    if approval_note:
        deal.approval_note = approval_note  # (Optional: Add field in model if needed)

    await deal.save()
    return {"message": f"Deal {deal_id} approved successfully."}

# === Reject a deal ===
@router.post("/reject-deal/{deal_id}")
async def reject_deal(
    deal_id: int,
    reason: Optional[str] = Body(None, embed=True),
    current_user=Depends(get_current_user),
):
    deal = await Deal.get_or_none(id=deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.status = "rejected"
    if reason:
        deal.rejection_reason = reason  # (Optional: Add field in model if needed)

    await deal.save()
    return {"message": f"Deal {deal_id} rejected."}
