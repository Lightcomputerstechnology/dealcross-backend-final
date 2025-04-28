# File: src/routers/disputes.py

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from tortoise.transactions import in_transaction

from core.security import get_current_user
from models.dispute import Dispute, DisputeStatus
from models.user import User
from schemas.dispute import DisputeCreate, DisputeResolve, DisputeOut

router = APIRouter(prefix="/disputes", tags=["Disputes"])

# ─────────── SUBMIT A DISPUTE ───────────

@router.post("/", response_model=DisputeOut, summary="Submit a dispute")
async def create_dispute(
    dispute: DisputeCreate,
    current_user: User = Depends(get_current_user),
) -> DisputeOut:
    new_dispute = await Dispute.create(
        deal_id=dispute.deal_id,
        user=current_user,
        reason=dispute.reason,
        details=dispute.details,
        status=DisputeStatus.open
    )
    return new_dispute

# ─────────── RESOLVE A DISPUTE ───────────

@router.put("/{dispute_id}/resolve", response_model=DisputeOut, summary="Resolve a dispute")
async def resolve_dispute(
    dispute_id: int,
    resolution: DisputeResolve,
    current_user: User = Depends(get_current_user),
) -> DisputeOut:
    dispute = await Dispute.get_or_none(id=dispute_id)

    if not dispute or dispute.status != DisputeStatus.open:
        raise HTTPException(status_code=400, detail="Cannot resolve this dispute.")

    dispute.status = DisputeStatus.resolved
    dispute.resolution = resolution.resolution
    dispute.resolved_at = datetime.utcnow()
    await dispute.save()

    return dispute
