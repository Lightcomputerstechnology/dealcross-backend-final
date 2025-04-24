from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User, UserRole
from models.logs import AuditLog
from schemas.user import UserOut
from schemas.logs import AuditLogOut
from sqlalchemy import func
from models.deal import Deal, DealStatus
from models.dispute import Dispute
from models.fee_transaction import FeeTransaction
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["Admin Controls"])

# ─────────── ADMIN CHECK ───────────
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# ─────────── LIST USERS ───────────
@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).all()

# ─────────── UPDATE USER ROLE ───────────
@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, new_role: UserRole, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.role = new_role
    db.commit()

    # Audit log
    audit = AuditLog(action=f"Role updated to {new_role} for user {user_id}", performed_by=admin.id)
    db.add(audit)
    db.commit()
    return {"message": f"User role updated to {new_role}"}

# ─────────── VIEW AUDIT LOGS ───────────
@router.get("/audit-logs", response_model=list[AuditLogOut])
def view_audit_logs(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()

# ─────────── DASHBOARD METRICS ───────────
@router.get("/dashboard-metrics", summary="Admin: Platform-wide dashboard metrics")
def admin_dashboard_metrics(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    now = datetime.utcnow()
    start_of_month = now.replace(day=1)
    last_month = (start_of_month - timedelta(days=1)).replace(day=1)

    # Users
    total_users = db.query(User).count()
    new_users_7d = db.query(User).filter(User.created_at >= now - timedelta(days=7)).count()

    # Deals
    total_deals = db.query(Deal).count()
    active_deals = db.query(Deal).filter(Deal.status == DealStatus.active).count()
    completed_deals = db.query(Deal).filter(Deal.status == DealStatus.completed).count()
    disputed_deals = db.query(Deal).filter(Deal.status == DealStatus.disputed).count()
    flagged_deals = db.query(Deal).filter(Deal.is_flagged == True).count()

    # Disputes
    dispute_statuses = db.query(Dispute.status, func.count(Dispute.id)).group_by(Dispute.status).all()
    dispute_breakdown = {status: count for status, count in dispute_statuses}
    total_disputes = sum(dispute_breakdown.values())
    disputes_this_month = db.query(Dispute).filter(Dispute.created_at >= start_of_month).count()
    disputes_last_month = db.query(Dispute).filter(Dispute.created_at >= last_month, Dispute.created_at < start_of_month).count()

    # Avg resolution time (days)
    resolution_times = db.query(func.avg(func.extract('epoch', Dispute.resolved_at - Dispute.created_at))).filter(Dispute.status == "resolved").scalar()
    avg_resolution_days = round((resolution_times or 0) / 86400, 2) if resolution_times else 0

    # Fees
    total_fees = db.query(func.sum(FeeTransaction.amount)).scalar() or 0.00
    monthly_fees = db.query(func.sum(FeeTransaction.amount)).filter(FeeTransaction.timestamp >= start_of_month).scalar() or 0.00

    return {
        "users": {"total": total_users, "new_last_7_days": new_users_7d},
        "deals": {"total": total_deals, "active": active_deals, "completed": completed_deals, "disputed": disputed_deals, "flagged": flagged_deals},
        "disputes": {
            "total": total_disputes,
            "status_breakdown": dispute_breakdown,
            "this_month": disputes_this_month,
            "last_month": disputes_last_month,
            "avg_resolution_days": avg_resolution_days
        },
        "fees": {"total_collected": total_fees, "collected_this_month": monthly_fees}
    }