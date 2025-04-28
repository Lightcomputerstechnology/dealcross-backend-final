Audit Log Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends from core.dependencies import require_admin from models.auditlog import AuditLog from schemas.audit import AuditLogOut from typing import List

router = APIRouter()

@router.get("/audit-logs", response_model=List[AuditLogOut]) async def get_audit_logs(admin=Depends(require_admin)): logs = await AuditLog.all().order_by("-timestamp") return logs

