# File: routers/admin.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.expressions import Q
from tortoise import fields

from core.security import get_current_user  # returns JWT claims (Supabase-aware)
from core.supabase_client import get_profile_is_admin  # server-side is_admin check

from models.user import User, UserRole
from models.auditlog import AuditLog
from models.deal import Deal, DealStatus
from models.dispute import Dispute
from models.feetransaction import FeeTransaction   # ⬅️ kept your import path as-is
from models.referral_reward import ReferralReward  # ✅ NEW

from schemas.user import UserOut
from schemas.logs import AuditLogOut

router = APIRouter(prefix="/admin", tags=["Admin Controls"])


# ───────────────────────── Helpers ─────────────────────────

async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    """
    Map verified JWT claims → local User row by email.
    We do NOT auto-create to avoid corrupting your schema.
    """
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


async def require_admin_from_supabase_or_local(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    """
    Admin check:
    1) Server-side read of Supabase public.profiles.is_admin (SERVICE ROLE).
    2) Fallback to local db_user.is_admin or role == admin.
    """
    supa_user_id = claims.get("sub")  # Supabase uses 'sub' as auth.users.id
    is_admin = False

    if supa_user_id:
        flag = get_profile_is_admin(supa_user_id)
        is_admin = bool(flag)

    if not is_admin:
        # Local fallbacks if you already store this
        if getattr(db_user, "is_admin", False) or getattr(db_user, "role", None) == UserRole.admin:
            is_admin = True

    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required.")

    return db_user


# ───────────────────────── Endpoints ─────────────────────────

# ─────────── LIST USERS ───────────
@router.get("/users", response_model=List[UserOut])
async def list_users(_: User = Depends(require_admin_from_supabase_or_local)):
    users = await User.all()
    return [await UserOut.from_tortoise_orm(u) for u in users]

# ─────────── UPDATE USER ROLE ───────────
@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    admin: User = Depends(require_admin_from_supabase_or_local),
):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.role = new_role
    await user.save()

    await AuditLog.create(
        action=f"Role updated to {new_role} for user {user_id}",
        performed_by=admin
    )
    return {"message": f"User role updated to {new_role}"}

# ─────────── VIEW AUDIT LOGS ───────────
@router.get("/audit-logs", response_model=List[AuditLogOut])
async def view_audit_logs(_: User = Depends(require_admin_from_supabase_or_local)):
    logs = await AuditLog.all().order_by("-timestamp")
    return [await AuditLogOut.from_tortoise_orm(l) for l in logs]

# ─────────── USER ACTIVITY LOGS ───────────
@router.get("/user-logs", summary="Admin: User activity logs", response_model=List[AuditLogOut])
async def get_user_logs(_: User = Depends(require_admin_from_supabase_or_local)):
    logs = await AuditLog.all().order_by("-timestamp").limit(100)
    return [await AuditLogOut.from_tortoise_orm(l) for l in logs]

# ─────────── DASHBOARD METRICS ───────────
@router.get("/dashboard-metrics", summary="Admin: Platform-wide dashboard metrics")
async def admin_dashboard_metrics(_: User = Depends(require_admin_from_supabase_or_local)):
    now = datetime.utcnow()
    start_of_month = now.replace(day=1)
    last_month = (start_of_month - timedelta(days=1)).replace(day=1)

    total_users = await User.all().count()
    new_users_7d = await User.filter(created_at__gte=now - timedelta(days=7)).count()

    total_deals = await Deal.all().count()
    active_deals = await Deal.filter(status=DealStatus.active).count()
    completed_deals = await Deal.filter(status=DealStatus.completed).count()
    disputed_deals = await Deal.filter(status=DealStatus.disputed).count()
    flagged_deals = await Deal.filter(is_flagged=True).count()

    dispute_statuses = await Dispute.all().group_by("status").annotate(count=fields.Count("id"))
    dispute_breakdown = {d.status: d.count for d in dispute_statuses}
    total_disputes = sum(dispute_breakdown.values())
    disputes_this_month = await Dispute.filter(created_at__gte=start_of_month).count()
    disputes_last_month = await Dispute.filter(created_at__gte=last_month, created_at__lt=start_of_month).count()

    resolved_disputes = await Dispute.filter(status="resolved", resolved_at__isnull=False).all()
    if resolved_disputes:
        total_seconds = sum([(d.resolved_at - d.created_at).total_seconds() for d in resolved_disputes])
        avg_resolution_days = round((total_seconds / len(resolved_disputes)) / 86400, 2)
    else:
        avg_resolution_days = 0

    total_fees = await FeeTransaction.all().aggregate(total=fields.Sum("amount"))
    monthly_fees = await FeeTransaction.filter(timestamp__gte=start_of_month).aggregate(total=fields.Sum("amount"))

    return {
        "users": {"total": total_users, "new_last_7_days": new_users_7d},
        "deals": {
            "total": total_deals,
            "active": active_deals,
            "completed": completed_deals,
            "disputed": disputed_deals,
            "flagged": flagged_deals
        },
        "disputes": {
            "total": total_disputes,
            "status_breakdown": dispute_breakdown,
            "this_month": disputes_this_month,
            "last_month": disputes_last_month,
            "avg_resolution_days": avg_resolution_days
        },
        "fees": {
            "total_collected": total_fees.get("total", 0.00),
            "collected_this_month": monthly_fees.get("total", 0.00)
        }
    }

# ─────────── REFERRAL BONUS LOGS ───────────
@router.get("/referral-bonuses", summary="Admin: View all referral bonus rewards")
async def get_all_referral_bonuses(_: User = Depends(require_admin_from_supabase_or_local)):
    bonuses = await ReferralReward.all().order_by("-created_at")
    return [
        {
            "id": bonus.id,
            "inviter_id": bonus.inviter_id,
            "invitee_id": bonus.invitee_id,
            "reward_amount": float(bonus.reward_amount),
            "event": bonus.event,
            "created_at": bonus.created_at.isoformat(),
        }
        for bonus in bonuses
    ]
