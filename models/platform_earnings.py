File: models/platform_earnings.py

from tortoise import fields, models from datetime import datetime

class PlatformEarning(models.Model): id = fields.IntField(pk=True) user = fields.ForeignKeyField("models.User", related_name="earnings") source = fields.CharField(max_length=50)  # funding, escrow, share_buy, share_sell amount = fields.DecimalField(max_digits=12, decimal_places=2) created_at = fields.DatetimeField(auto_now_add=True)

class Meta:
    table = "platform_earnings"
    ordering = ["-created_at"]

def __str__(self):
    return f"{self.source} | {self.amount} | {self.user_id}"

