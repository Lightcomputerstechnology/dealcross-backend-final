# File: src/models/admin_wallet_log.py

from tortoise import fields, models

class AdminWalletLog(models.Model):
    id = fields.IntField(pk=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    action = fields.CharField(max_length=50)  # e.g., "fee_credit", "referral_reward", "manual_adjustment"
    description = fields.TextField(null=True)
    admin_wallet = fields.ForeignKeyField("models.AdminWallet", related_name="logs")
    triggered_by = fields.ForeignKeyField("models.User", null=True, related_name="wallet_logs")  # admin or system user
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admin_wallet_logs"

    def __str__(self):
        return f"{self.action.upper()} - ${self.amount} at {self.created_at}"