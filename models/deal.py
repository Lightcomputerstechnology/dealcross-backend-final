# File: models/deal.py

from tortoise import Model, fields
from models.user import User  # Ensure proper import if needed

# ─────────── DEAL MODEL ───────────

class Deal(Model):
    id = fields.IntField(pk=True)
    
    # Creator of the deal (the one who initiated it)
    creator = fields.ForeignKeyField(
        "models.User",
        related_name="created_deals",
        on_delete=fields.CASCADE
    )

    # Counterparty (the user being paired with or seller/buyer)
    counterparty = fields.ForeignKeyField(
        "models.User",
        related_name="paired_deals",
        null=True,
        on_delete=fields.SET_NULL
    )

    title = fields.CharField(max_length=200, null=True)
    description = fields.TextField(null=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    
    status = fields.CharField(max_length=50, default="pending")  # pending, active, completed, disputed, etc.
    
    is_public = fields.BooleanField(default=True)
    pairing_confirmed = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Deal(id={self.id}, status={self.status})"