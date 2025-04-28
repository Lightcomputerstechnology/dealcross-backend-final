KYC Model (Tortoise ORM Version)

from tortoise import fields from tortoise.models import Model import enum

class KYCStatus(str, enum.Enum): pending  = "pending" approved = "approved" rejected = "rejected"

class KYC(Model): id            = fields.IntField(pk=True) user          = fields.ForeignKeyField("models.User", related_name="kyc_requests", on_delete=fields.CASCADE) document_type = fields.CharField(max_length=255) document_url  = fields.CharField(max_length=255) status        = fields.CharEnumField(KYCStatus, default=KYCStatus.pending) submitted_at  = fields.DatetimeField(auto_now_add=True)

# ——— Admin review fields ———
review_note   = fields.TextField(null=True)
reviewed_by   = fields.ForeignKeyField("models.User", related_name="reviewed_kyc", null=True)
reviewed_at   = fields.DatetimeField(null=True)

