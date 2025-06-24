from tortoise import Model, fields

# ─────────── DEAL PAIRING MODEL ───────────

class Pairing(Model):
    id = fields.IntField(pk=True)

    creator = fields.ForeignKeyField(
        "models.User",  # ✅ Corrected to "app.Model"
        related_name="created_pairings",
        on_delete=fields.CASCADE
    )

    counterparty = fields.ForeignKeyField(
        "models.User",  # ✅ Corrected to "app.Model"
        related_name="received_pairings",
        on_delete=fields.CASCADE
    )

    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Pairing(creator={self.creator_id}, counterparty={self.counterparty_id}, status={self.status})"