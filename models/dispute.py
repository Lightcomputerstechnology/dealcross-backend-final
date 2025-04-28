# File: src/models/dispute.py

from tortoise import fields
from tortoise.models import Model
import enum

# Dispute Status Enum
class DisputeStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"

# Dispute Model
class Dispute(Model):
    id = fields.IntField(pk=True)
    deal_id = fields.IntField()  # Assuming you store the related deal ID directly
    user = fields.ForeignKeyField("models.User", related_name="disputes", on_delete=fields.CASCADE)
    reason = fields.CharField(max_length=255)
    details = fields.TextField()
    status = fields.CharEnumField(DisputeStatus, default=DisputeStatus.open)
    resolution = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    resolved_at = fields.DatetimeField(null=True)
