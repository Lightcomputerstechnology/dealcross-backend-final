# File: models/fraud.py

from tortoise.models import Model
from tortoise import fields
import enum

class FraudStatus(str, enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    resolved = "resolved"

class FraudAlert(Model):
    id = fields.IntField(pk=True)

    deal = fields.ForeignKeyField(
        "models.Deal",
        related_name="fraud_alerts",
        on_delete=fields.CASCADE,
        defer_fk=True  # ✅ added to break cyclic FK creation issues
    )

    reporter = fields.ForeignKeyField(
        "models.User",
        related_name="reported_frauds",
        on_delete=fields.CASCADE
    )

    reason = fields.CharField(max_length=255)
    status = fields.CharEnumField(FraudStatus, default=FraudStatus.pending)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "fraud_alerts"

    def __str__(self):
        return f"Fraud reported by {self.reporter_id} on Deal {self.deal_id}"