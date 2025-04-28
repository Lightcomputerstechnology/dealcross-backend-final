# File: app/api/routes/admin/auditlog.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from core.security import get_current_user
from models.audit_log import AuditLog
from schemas.audit_schema import AuditLogOut

router = APIRouter(prefix="/admin/audit-logs", tags=["Admin - Audit Logs"])

@router.get("/", response_model=List[AuditLogOut])
async def fetch_audit_logs(current_user=Depends(get_current_user)):
    """
    Get recent admin actions for transparency and monitoring.
    """
    try:
        logs = await AuditLog.all().order_by("-created_at").limit(50)
        return [AuditLogOut.model_validate(log) for log in logs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")
