from tortoise import fields
from tortoise.models import Model
import enum

class DisputeStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"

class Dispute(Model):
    id = fields.IntField(pk=True)

    # deal = fields.ForeignKeyField(
    #     "models.Deal",
    #     related_name="disputes",
    #     on_delete=fields.CASCADE,
    #     defer_fk=True
    # )
    deal_id = fields.IntField(null=True)  # 🚩 temporary replacement

    # user = fields.ForeignKeyField(
    #     "models.User",
    #     related_name="disputes",
    #     on_delete=fields.CASCADE
    # )
    user_id = fields.IntField(null=True)  # 🚩 temporary replacement

    reason = fields.CharField(max_length=255)
    details = fields.TextField()
    status = fields.CharEnumField(DisputeStatus, default=DisputeStatus.open)
    resolution = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    resolved_at = fields.DatetimeField(null=True)

    class Meta:
        table = "disputes"