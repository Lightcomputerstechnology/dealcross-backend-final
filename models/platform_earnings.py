from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class PlatformEarning(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="platform_earnings",
        on_delete=fields.CASCADE
    )

    source = fields.CharField(
        max_length=50
    )  # E.g., 'funding', 'escrow', 'share_buy', etc.

    amount = fields.DecimalField(
        max_digits=12, decimal_places=2
    )

    note = fields.TextField(null=True)  # Optional extra explanation

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "platform_earnings"
        ordering = ["-created_at"]
        indexes = [("user_id", "source")]

    def __str__(self):
        return f"Earning(user={self.user_id}, {self.source}, ₦{self.amount})"

# Optional Pydantic version
PlatformEarning_Pydantic = pydantic_model_creator(PlatformEarning, name="PlatformEarning")