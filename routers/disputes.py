Disputes Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from core.security import get_current_user from models.dispute import Dispute, DisputeStatus from schemas.dispute import DisputeCreate, DisputeResolve, DisputeOut from tortoise.transactions import in_transaction from datetime import datetime

router = APIRouter(prefix="/disputes", tags=["Disputes"])

@router.post("/", response_model=DisputeOut, summary="Submit a dispute") async def create_dispute( dispute: DisputeCreate, current_user = Depends(get_current_user), ): new_dispute = await Dispute.create( deal_id=dispute.deal_id, user=current_user, reason=dispute.reason, details=dispute.details, status=DisputeStatus.open ) return new_dispute

@router.put("/{dispute_id}/resolve", response_model=DisputeOut, summary="Resolve a dispute") async def resolve_dispute( dispute_id: int, resolution: DisputeResolve, current_user = Depends(get_current_user), ): d = await Dispute.get_or_none(id=dispute_id) if not d or d.status != DisputeStatus.open: raise HTTPException(status_code=400, detail="Cannot resolve this dispute.")

d.status = DisputeStatus.resolved
d.resolution = resolution.resolution
d.resolved_at = datetime.utcnow()
await d.save()
return d

