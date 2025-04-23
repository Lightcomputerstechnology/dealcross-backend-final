from sqlalchemy import func
from models.user import User
from models.deal import Deal, DealStatus
from models.dispute import Dispute
from models.fee_transaction import FeeTransaction
from datetime import datetime, timedelta

@router.get("/dashboard-metrics", summary="Admin: Platform-wide dashboard metrics")
def admin_dashboard_metrics(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Returns key platform-wide metrics:

    - Users (total, new last 7 days)
    - Deals (total, active, completed, disputed, flagged)
    - Disputes (status breakdown, trends, avg resolution time)
    - Fees collected (all time, this month)
    """
    now = datetime.utcnow()
    start_of_month = now.replace(day=1)
    last_month = (start_of_month - timedelta(days=1)).replace(day=1)

    # User metrics
    total_users = db.query(User).count()
    new_users_7d = db.query(User).filter(User.created_at >= now - timedelta(days=7)).count()

    # Deal metrics
    total_deals = db.query(Deal).count()
    active_deals = db.query(Deal).filter(Deal.status == DealStatus.active).count()
    completed_deals = db.query(Deal).filter(Deal.status == DealStatus.completed).count()
    disputed_deals = db.query(Deal).filter(Deal.status == DealStatus.disputed).count()
    flagged_deals = db.query(Deal).filter(Deal.is_flagged == True).count()

    # Dispute metrics (status breakdown)
    dispute_statuses = db.query(Dispute.status, func.count(Dispute.id)).group_by(Dispute.status).all()
    dispute_breakdown = {status: count for status, count in dispute_statuses}

    total_disputes = sum(dispute_breakdown.values())
    disputes_this_month = db.query(Dispute).filter(Dispute.created_at >= start_of_month).count()
    disputes_last_month = db.query(Dispute).filter(Dispute.created_at >= last_month, Dispute.created_at < start_of_month).count()

    # Avg resolution time (in days)
    resolution_times = db.query(
        func.avg(func.extract('epoch', Dispute.resolved_at - Dispute.created_at))
    ).filter(Dispute.status == "resolved").scalar()
    avg_resolution_days = round((resolution_times or 0) / 86400, 2) if resolution_times else 0

    # Fee metrics
    total_fees = db.query(func.sum(FeeTransaction.amount)).scalar() or 0.00
    monthly_fees = db.query(func.sum(FeeTransaction.amount)).filter(FeeTransaction.timestamp >= start_of_month).scalar() or 0.00

    return {
        "users": {
            "total": total_users,
            "new_last_7_days": new_users_7d
        },
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
            "total_collected": total_fees,
            "collected_this_month": monthly_fees
        }
    }
