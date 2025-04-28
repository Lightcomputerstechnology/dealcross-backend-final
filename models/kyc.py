# File: src/models/kyc.py

from tortoise import fields
from tortoise.models import Model
import enum

class KYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCRequest(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="kyc_requests", on_delete=fields.CASCADE
    )
    document_type = fields.CharField(max_length=255)
    document_url = fields.CharField(max_length=255)
    status = fields.CharEnumField(KYCStatus, default=KYCStatus.pending)
    submitted_at = fields.DatetimeField(auto_now_add=True)
    reviewed_by = fields.ForeignKeyField(
        "models.User", related_name="kyc_reviews", null=True, on_delete=fields.SET_NULL
    )
    review_note = fields.TextField(null=True)

    class Meta:
        table = "kyc_requests"
