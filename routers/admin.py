from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.deal import Deal
from models.dispute import Dispute
from models.admin_wallet import AdminWallet  # ✅ Import admin wallet
from core.dependencies import require_admin  # ✅ Admin role check

router = APIRouter(prefix="/admin", tags=["Admin Core"])  # ✅ Tag added

# === Admin: Check wallet balance ===
@router.get("/wallet-balance", summary="Admin: View admin wallet balance")
def get_admin_wallet_balance(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """
    Allows an admin to view the current balance of the admin wallet.
    """
    wallet = db.query(AdminWallet).first()
    if not wallet:
        return {"balance": 0.00}
    return {"balance": float(wallet.balance)}

# === List all registered users ===
@router.get("/users", summary="Admin: View all registered users")
def list_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """
    Allows an admin to view all registered users in the system,
    including their roles and account status.
    """
    users = db.query(User).all()
    return [
        {
            "username": u.username,
            "email": u.email,
            "role": u.role.value if hasattr(u, "role") else "user",
            "status": u.status
        } for u in users
    ]

# === Admin analytics summary ===
@router.get("/analytics", summary="Admin: System-wide user and deal metrics")
def analytics_summary(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """
    Returns a summary of core platform metrics:

    - **users**: Total number of registered users.
    - **deals**: Total number of deals created.
    - **wallets_funded**: Users with non-zero wallet balance (if tracked).
    - **disputes**: Number of disputes raised.
    """
    return {
        "users": db.query(User).count(),
        "deals": db.query(Deal).count(),
        "wallets_funded": db.query(User).filter(User.wallet_balance > 0).count() if hasattr(User, "wallet_balance") else "N/A",
        "disputes": db.query(Dispute).count()
    }
