from tortoise import fields, models

class Pairing(models.Model):
    id = fields.IntField(pk=True)

    creator = fields.ForeignKeyField(
        "models.User",
        related_name="created_pairings",
        on_delete=fields.CASCADE,
    )

    counterparty = fields.ForeignKeyField(
        "models.User",
        related_name="received_pairings",
        on_delete=fields.CASCADE,
    )

    # If a pairing should be linked to a deal, keep a single FK from here to Deal:
    deal = fields.ForeignKeyField(
        "models.Deal",
        related_name="pairings",
        null=True,
        on_delete=fields.SET_NULL,
    )

    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "pairings"

    def __str__(self) -> str:
        return f"Pairing(creator={self.creator_id}, counterparty={self.counterparty_id}, status={self.status})"