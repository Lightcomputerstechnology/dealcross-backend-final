from typing import Optional
from tortoise import fields, models

class Deal(models.Model):
    id = fields.IntField(pk=True)

    creator = fields.ForeignKeyField(
        "models.User",
        related_name="created_deals",
        on_delete=fields.CASCADE,
    )

    counterparty = fields.ForeignKeyField(
        "models.User",
        related_name="paired_deals",
        null=True,
        on_delete=fields.SET_NULL,
    )

    title = fields.CharField(max_length=200, null=True)
    description = fields.TextField(null=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    escrow_locked = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    status = fields.CharField(max_length=50, default="pending")
    is_public = fields.BooleanField(default=True)
    pairing_confirmed = fields.BooleanField(default=False)

    # Reverse relations (no DB columns created here)
    escrow_trackers: fields.ReverseRelation["EscrowTracker"]
    # If your Pairing model points to Deal, you can also expose:
    pairings: fields.ReverseRelation["Pairing"]

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "deals"

    def __str__(self) -> str:
        return f"Deal(id={self.id}, status={self.status})"