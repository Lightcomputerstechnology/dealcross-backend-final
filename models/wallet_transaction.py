from tortoise import models, fields

class WalletTransaction(models.Model):
    id = fields.IntField(pk=True)
    
    wallet = fields.ForeignKeyField(
        "models.Wallet",  # ✅ Correct format
        related_name="transactions",
        on_delete=fields.CASCADE
    )
    
    user = fields.ForeignKeyField(
        "models.User",  # ✅ Correct format
        related_name="wallet_transactions",
        on_delete=fields.CASCADE
    )

    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = fields.CharField(max_length=50)  # e.g., fund, spend, transfer
    description = fields.CharField(max_length=255, null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "wallet_transactions"

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by user {self.user_id}"