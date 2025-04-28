Fraud Alerts / Logs Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from models.fraudalert import FraudAlert, FraudStatus from models.auditlog import AuditLog from models.user import User from schemas.logs import FraudAlertCreate, FraudAlertOut from core.security import get_current_user

router = APIRouter(prefix="/fraud", tags=["Fraud Alerts / Logs"])

─────────── REPORT FRAUD ───────────

@router.post("/report", response_model=FraudAlertOut) async def report_fraud(alert_in: FraudAlertCreate, current_user: User = Depends(get_current_user)): alert = await FraudAlert.create( deal_id=alert_in.deal_id, reporter=current_user, reason=alert_in.reason )

# Add to audit log
await AuditLog.create(
    action=f"Fraud reported on deal {alert_in.deal_id}",
    performed_by=current_user
)

return alert

─────────── VIEW FRAUD ALERTS (ADMIN) ───────────

@router.get("/alerts", response_model=list[FraudAlertOut]) async def view_fraud_alerts(current_user: User = Depends(get_current_user)): if current_user.role != "admin": raise HTTPException(status_code=403, detail="Admin access required.")

return await FraudAlert.all()

