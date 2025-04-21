# File: app/api/routes/admin/auditlog.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.audit_log import AuditLog
from schemas.audit_schema import AuditLogOut

router = APIRouter()

@router.get("/audit-logs", response_model=List[AuditLogOut])
def fetch_audit_logs(db: Session = Depends(get_db)):
    """
    Get recent admin actions for transparency and monitoring.
    """
    try:
        return (
            db.query(AuditLog)
            .order_by(AuditLog.timestamp.desc())
            .limit(50)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")
