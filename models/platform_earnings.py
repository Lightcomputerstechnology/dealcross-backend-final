from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class PlatformEarnings(models.Model):  # ✅ Renamed to match __init__.py
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",  # ✅ Correct format
        related_name="platform_earnings",
        on_delete=fields.CASCADE
    )

    source = fields.CharField(max_length=50)  # e.g., 'funding', 'escrow', etc.

    amount = fields.DecimalField(max_digits=12, decimal_places=2)

    note = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "platform_earnings"
        ordering = ["-created_at"]
        indexes = [("user_id", "source")]

    def __str__(self):
        return f"Earning(user={self.user_id}, {self.source}, ₦{self.amount})"

# Optional Pydantic version
PlatformEarnings_Pydantic = pydantic_model_creator(PlatformEarnings, name="PlatformEarnings")