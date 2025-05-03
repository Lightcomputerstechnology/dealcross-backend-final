# File: models/platform_earnings.py

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class PlatformEarning(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="platform_earnings")
    source = fields.CharField(max_length=50)  # e.g. 'funding', 'escrow', 'share_buy', 'share_sell'
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    note = fields.TextField(null=True)  # Optional: explanation or metadata
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "platform_earnings"
        ordering = ["-timestamp"]
        indexes = [("user_id", "source")]

    def __str__(self):
        return f"Earning(user={self.user_id}, source={self.source}, amount={self.amount})"

# Optional: Pydantic output if needed in routers
PlatformEarning_Pydantic = pydantic_model_creator(PlatformEarning, name="PlatformEarning")