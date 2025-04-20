# File: routers/admin_controls.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.deal import Deal

router = APIRouter()

# Approve Deal Endpoint
@router.post("/deal/{deal_id}/approve")
def approve_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "approved"
    db.commit()
    return {"message": "Deal approved successfully."}

# Ban User Endpoint
@router.post("/user/{user_id}/ban")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "banned"
    db.commit()
    return {"message": "User has been banned."}

# Admin Audit Logs Endpoint
@router.get("/admin/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    from models.admin_log import AdminAuditLog  # import inline to avoid circular imports
    logs = db.query(AdminAuditLog).order_by(AdminAuditLog.timestamp.desc()).limit(100).all()
    return logs
                            
