# File: models/pending_approval.py

from datetime import datetime
from enum import Enum
from tortoise import fields
from tortoise.models import Model

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PendingApproval(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="pending_approvals")
    approval_type = fields.CharField(max_length=50)  # e.g., "kyc", "deal"
    related_object_id = fields.IntField()  # Reference ID (KYC/Deal)
    status = fields.CharEnumField(ApprovalStatus, default=ApprovalStatus.PENDING)
    reason = fields.TextField(null=True)
    reviewed_by = fields.ForeignKeyField("models.User", null=True, related_name="reviewed_approvals")
    reviewed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "pending_approvals"
        ordering = ["-created_at"]
        indexes = [("approval_type", "status")]

    def __str__(self):
        return f"{self.approval_type.upper()} | {self.status}"