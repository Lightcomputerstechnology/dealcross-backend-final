# File: utils/logger.py

from sqlalchemy.orm import Session
from models.audit import AuditLog
from models import User

def log_admin_action(db: Session, admin_user: User, action: str, target_type: str, target_id: int):
    log = AuditLog(
        admin_id=admin_user.id,
        action=action,
        target_type=target_type,
        target_id=target_id
    )
    db.add(log)
    db.commit()
