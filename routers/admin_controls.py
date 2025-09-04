from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user            # Supabase-aware claims
from core.supabase_client import get_profile_is_admin # server-side admin check

from models.user import User
from models.deal import Deal
from schemas.admin_controls import BlockAction, DealApproval

router = APIRouter(prefix="/admin/controls", tags=["Admin Controls"])


# Map verified JWT claims → local DB User
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user

# Admin guard (Supabase profiles.is_admin or local role/flag)
async def require_admin(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    supa_user_id = claims.get("sub")
    is_admin = False
    if supa_user_id:
        is_admin = bool(get_profile_is_admin(supa_user_id))
    if not is_admin and (getattr(db_user, "is_admin", False) or getattr(db_user, "role", "") == "admin"):
        is_admin = True
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")
    return db_user


# === Get all users ===
@router.get("/users")
async def get_users(_: User = Depends(require_admin)):
    users = await User.all().order_by("-created_at")
    return [
        {
            "id": u.id,
            "email": getattr(u, "email", None),
            "username": getattr(u, "username", None),
            "role": getattr(u, "role", None),
            "is_blocked": getattr(u, "is_blocked", False),
            "created_at": getattr(u, "created_at", None),
        }
        for u in users
    ]


# === Block a user ===
@router.post("/users/block")
async def block_user(data: BlockAction, _: User = Depends(require_admin)):
    user = await User.get_or_none(id=data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_blocked = True
    setattr(user, "block_reason", data.reason if hasattr(user, "block_reason") else None)
    await user.save()
    return {"message": "User blocked successfully."}


# === Unblock a user ===
@router.post("/users/unblock")
async def unblock_user(data: BlockAction, _: User = Depends(require_admin)):
    user = await User.get_or_none(id=data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_blocked = False
    if hasattr(user, "block_reason"):
        user.block_reason = None
    await user.save()
    return {"message": "User unblocked successfully."}


# === Approve a deal ===
@router.post("/deals/approve")
async def approve_deal(data: DealApproval, _: User = Depends(require_admin)):
    deal = await Deal.get_or_none(id=data.deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "approved"
    if hasattr(deal, "approval_note"):
        deal.approval_note = data.note
    await deal.save()
    return {"message": "Deal approved."}


# === Reject a deal ===
@router.post("/deals/reject")
async def reject_deal(data: DealApproval, _: User = Depends(require_admin)):
    deal = await Deal.get_or_none(id=data.deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "rejected"
    if hasattr(deal, "approval_note"):
        deal.approval_note = data.note
    await deal.save()
    return {"message": "Deal rejected."}
