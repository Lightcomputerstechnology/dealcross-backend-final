from sqlalchemy import func
from models.user import User
from models.deal import Deal, DealStatus
from models.dispute import Dispute
from models.fee_transaction import FeeTransaction, FeeType
from datetime import datetime, timedelta

# === Admin: Dashboard metrics ===
@router.get("/dashboard-metrics", summary="Admin: Platform-wide dashboard metrics")
def admin_dashboard_metrics(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Returns key platform-wide metrics:

    - Users (total, new last 7 days)
    - Deals (total, active, completed, disputed, flagged)
    - Disputes (total, resolved, unresolved)
    - Fees collected (all time, this month)
    """
    # User metrics
    total_users = db.query(User).count()
    new_users_7d = db.query(User).filter(User.created_at >= datetime.utcnow() - timedelta(days=7)).count()

    # Deal metrics
    total_deals = db.query(Deal).count()
    active_deals = db.query(Deal).filter(Deal.status == DealStatus.active).count()
    completed_deals = db.query(Deal).filter(Deal.status == DealStatus.completed).count()
    disputed_deals = db.query(Deal).filter(Deal.status == DealStatus.disputed).count()
    flagged_deals = db.query(Deal).filter(Deal.is_flagged == True).count()

    # Dispute metrics
    total_disputes = db.query(Dispute).count()
    resolved_disputes = db.query(Dispute).filter(Dispute.status == "resolved").count()
    unresolved_disputes = total_disputes - resolved_disputes

    # Fee metrics
    total_fees = db.query(func.sum(FeeTransaction.amount)).scalar() or 0.00
    start_of_month = datetime.utcnow().replace(day=1)
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
            "resolved": resolved_disputes,
            "unresolved": unresolved_disputes
        },
        "fees": {
            "total_collected": total_fees,
            "collected_this_month": monthly_fees
        }
    }
