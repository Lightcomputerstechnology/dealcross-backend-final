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

    # Who made the request
    user = fields.ForeignKeyField("models.User", related_name="pending_approvals")

    # What is being reviewed (e.g., KYC, Deal)
    approval_type = fields.CharField(max_length=50)
    related_object_id = fields.IntField()

    # Review Status
    status = fields.CharEnumField(ApprovalStatus, default=ApprovalStatus.PENDING)
    reason = fields.TextField(null=True)

    # Admin reviewing it
    reviewed_by = fields.ForeignKeyField("models.User", null=True, related_name="reviewed_approvals")
    reviewed_at = fields.DatetimeField(null=True)

    # Audit trail
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "pending_approvals"
        ordering = ["-created_at"]
        indexes = [("approval_type", "status")]

    def __str__(self):
        return f"{self.approval_type.upper()} Request by User {self.user_id} - {self.status}"