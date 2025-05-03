# File: src/models/admin_wallet.py

from tortoise import fields
from tortoise.models import Model

class AdminWallet(Model):
    id = fields.IntField(pk=True)
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = fields.CharField(max_length=10, default="USD")  # Multi-currency support
    last_updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="admin_wallet_updates",
        null=True,
        on_delete=fields.SET_NULL
    )
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "admin_wallet"

    def __str__(self):
        return f"AdminWallet(id={self.id}, balance={self.balance}, currency={self.currency})"