from tortoise.models import Model
from tortoise import fields
import enum

class FeeType(str, enum.Enum):
    funding = "funding"
    escrow = "escrow"
    share_buy = "share_buy"
    share_sell = "share_sell"

class FeeTransaction(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",  # ✅ FIXED: Correct format
        related_name="fee_transactions",
        null=True,
        on_delete=fields.SET_NULL
    )

    fee_type = fields.CharEnumField(FeeType)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "fee_transactions"

    def __str__(self):
        return f"FeeTransaction(user={self.user_id}, type={self.fee_type}, amount={self.amount})"