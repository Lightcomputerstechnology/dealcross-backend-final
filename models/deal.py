


from tortoise import fields, models

class Deal(models.Model):
    id = fields.IntField(pk=True)

    creator = fields.ForeignKeyField(
        "models.user.User",  # ✅ Fully qualified
        related_name="created_deals",
        on_delete=fields.CASCADE
    )

    counterparty = fields.ForeignKeyField(
        "models.user.User",  # ✅ Fully qualified
        related_name="paired_deals",
        null=True,
        on_delete=fields.SET_NULL
    )

    title = fields.CharField(max_length=200, null=True)
    description = fields.TextField(null=True)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    escrow_locked = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    status = fields.CharField(max_length=50, default="pending")
    is_public = fields.BooleanField(default=True)
    pairing_confirmed = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Deal(id={self.id}, status={self.status})"