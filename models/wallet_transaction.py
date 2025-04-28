# File: src/models/wallet_transaction.py

from tortoise.models import Model
from tortoise import fields
from models.user import User
from models.wallet import Wallet

class WalletTransaction(Model):
    id = fields.IntField(pk=True)
    wallet = fields.ForeignKeyField("models.Wallet", related_name="transactions")
    user = fields.ForeignKeyField("models.User", related_name="wallet_transactions")
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = fields.CharField(max_length=50)  # Example: fund, spend, refund
    description = fields.TextField(null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "wallet_transactions"  # Optional: Custom table name if you want

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} USD"
