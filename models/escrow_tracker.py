from tortoise.models import Model
from tortoise import fields
class EscrowTracker(Model):
    id = fields.IntField(pk=True)
    deal = fields.ForeignKeyField("models.Deal", related_name="escrows", on_delete=fields.CASCADE)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    status = fields.CharField(max_length=255, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)
