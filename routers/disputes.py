from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user                 # Supabase-aware claims (verified via JWKS)
from core.supabase_client import get_profile_is_admin      # server-side admin check (SERVICE ROLE)
from models.dispute import Dispute, DisputeStatus
from models.user import User
from schemas.dispute import DisputeCreate, DisputeResolve, DisputeOut

router = APIRouter(prefix="/disputes", tags=["Disputes"])


# Map verified JWT claims → local DB User
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


def _claims_is_admin(claims: Dict[str, Any]) -> bool:
    supa_user_id = claims.get("sub")
    if not supa_user_id:
        return False
    return bool(get_profile_is_admin(supa_user_id))


# ─────────── SUBMIT A DISPUTE ───────────
@router.post("/", response_model=DisputeOut, summary="Submit a dispute")
async def create_dispute(
    dispute: DisputeCreate,
    current_user: User = Depends(resolve_db_user),
) -> DisputeOut:
    new_dispute = await Dispute.create(
        deal_id=dispute.deal_id,
        user=current_user,
        reason=dispute.reason,
        details=dispute.details,
        status=DisputeStatus.open,
        created_at=datetime.utcnow()  # if your model has auto_add, this is harmless
    )
    return await DisputeOut.from_tortoise_orm(new_dispute)


# ─────────── RESOLVE A DISPUTE ───────────
@router.put("/{dispute_id}/resolve", response_model=DisputeOut, summary="Resolve a dispute")
async def resolve_dispute(
    dispute_id: int,
    resolution: DisputeResolve,
    claims: Dict[str, Any] = Depends(get_current_user),
    current_user: User = Depends(resolve_db_user),
) -> DisputeOut:
    dispute = await Dispute.get_or_none(id=dispute_id).prefetch_related("user")
    if not dispute or dispute.status != DisputeStatus.open:
        raise HTTPException(status_code=400, detail="Cannot resolve this dispute.")

    # Allow only the dispute owner or an admin
    is_admin = _claims_is_admin(claims)
    is_owner = getattr(dispute.user, "id", None) == getattr(current_user, "id", None)
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not permitted to resolve this dispute.")

    dispute.status = DisputeStatus.resolved
    dispute.resolution = resolution.resolution
    dispute.resolved_at = datetime.utcnow()
    await dispute.save()

    return await DisputeOut.from_tortoise_orm(dispute)
