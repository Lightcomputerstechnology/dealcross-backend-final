# File: routers/auditlog.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import require_admin
from models.audit import AuditLog
from schemas.audit import AuditLogOut
from typing import List

router = APIRouter()

@router.get("/audit-logs", response_model=List[AuditLogOut])
def get_audit_logs(db: Session = Depends(get_db), admin=Depends(require_admin)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    return logs
