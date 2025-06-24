from tortoise import models, fields

class Wallet(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",  # ✅ Correct format: "models.Model"
        related_name="wallet",
        on_delete=fields.CASCADE
    )

    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "wallets"

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance} USD"