from tortoise import models, fields
import enum

class KYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCRequest(models.Model):
    id = fields.IntField(pk=True)

    # user = fields.ForeignKeyField(
    #     "models.User",
    #     related_name="kyc_requests",
    #     on_delete=fields.CASCADE
    # )
    user_id = fields.IntField(null=True)  # 🚩 temporary replacement

    document_type = fields.CharField(max_length=50)  # e.g., "passport", "id_card"
    document_number = fields.CharField(max_length=100)
    document_image_url = fields.CharField(max_length=255)
    status = fields.CharEnumField(KYCStatus, default=KYCStatus.pending)
    submitted_at = fields.DatetimeField(auto_now_add=True)
    reviewed_at = fields.DatetimeField(null=True)

    # reviewed_by = fields.ForeignKeyField(
    #     "models.User",
    #     related_name="reviewed_kyc_requests",
    #     on_delete=fields.SET_NULL,
    #     null=True
    # )
    reviewed_by_id = fields.IntField(null=True)  # 🚩 temporary replacement

    notes = fields.TextField(null=True)

    class Meta:
        table = "kyc_requests"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"KYC {self.id} for User {self.user_id} [{self.status}]"