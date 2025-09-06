# File: routers/admin.py

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from core.security import get_current_user
from models.user import User, UserRole
# 🔁 FIX: import AuditLog from the correct module name.
#    If your file is models/audit_log.py, keep this import.
#    If your file is models/audit.py instead, change to: from models.audit import AuditLog
from models.audit_log import AuditLog

from models.deal import Deal, DealStatus
from models.dispute import Dispute
from models.fee_transaction import FeeTransaction
from models.referral_reward import ReferralReward
from schemas.user import UserOut
from schemas.logs import AuditLogOut
from datetime import datetime, timedelta
from tortoise.expressions import Q
from tortoise import fields

router = APIRouter(prefix="/admin", tags=["Admin Controls"])

# ─────────── ADMIN CHECK ───────────
async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# ─────────── LIST USERS ───────────
@router.get("/users", response_model=list[UserOut])
async def list_users(admin: User = Depends(require_admin)):
    return await User.all()

# ─────────── UPDATE USER ROLE ───────────
@router.put("/users/{user_id}/role")
async def update_user_role(user_id: int, new_role: UserRole, admin: User = Depends(require_admin)):
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
@router.get("/audit-logs", response_model=list[AuditLogOut])
async def view_audit_logs(admin: User = Depends(require_admin)):
    return await AuditLog.all().order_by("-timestamp")

# ─────────── USER ACTIVITY LOGS ───────────
@router.get("/user-logs", summary="Admin: User activity logs", response_model=list[AuditLogOut])
async def get_user_logs(admin: User = Depends(require_admin)):
    return await AuditLog.all().order_by("-timestamp").limit(100)

# ─────────── DASHBOARD METRICS ───────────
@router.get("/dashboard-metrics", summary="Admin: Platform-wide dashboard metrics")
async def admin_dashboard_metrics(admin: User = Depends(require_admin)):
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
async def get_all_referral_bonuses(admin: User = Depends(require_admin)):
    rewards = await ReferralReward.all().order_by("-created_at")
    return [
        {
            "id": r.id,
            "inviter_id": r.inviter_id,
            "invitee_id": r.invitee_id,
            "reward_amount": float(r.reward_amount),
            "event": r.event,
            "created_at": r.created_at.isoformat(),
        }
        for r in rewards
    ]