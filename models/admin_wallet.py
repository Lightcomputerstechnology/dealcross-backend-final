# File: src/models/admin_wallet.py

from tortoise.models import Model
from tortoise import fields

class AdminWallet(Model):
    id = fields.IntField(pk=True)
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "admin_wallet"

    def __str__(self):
        return f"AdminWallet(id={self.id}, balance={self.balance})"
