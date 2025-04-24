from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.logs import FraudAlert, AuditLog, FraudStatus
from models.user import User
from schemas.logs import FraudAlertCreate, FraudAlertOut
from core.security import get_current_user

router = APIRouter(prefix="/fraud", tags=["Fraud Alerts / Logs"])

# ─────────── REPORT FRAUD ───────────
@router.post("/report", response_model=FraudAlertOut)
def report_fraud(alert_in: FraudAlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = FraudAlert(
        deal_id=alert_in.deal_id,
        reporter_id=current_user.id,
        reason=alert_in.reason
    )
    db.add(alert)

    # Add to audit log
    audit = AuditLog(
        action=f"Fraud reported on deal {alert_in.deal_id}",
        performed_by=current_user.id
    )
    db.add(audit)
    db.commit()
    db.refresh(alert)
    return alert

# ─────────── VIEW FRAUD ALERTS (ADMIN) ───────────
@router.get("/alerts", response_model=list[FraudAlertOut])
def view_fraud_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    
    return db.query(FraudAlert).all()