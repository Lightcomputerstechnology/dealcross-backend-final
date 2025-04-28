from tortoise import Model, fields

# ─────────── DEAL MODEL ───────────

class Deal(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="deals",
        on_delete=fields.CASCADE
    )
    status = fields.CharField(max_length=50)  # Optimized field size for status
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Deal(id={self.id}, status={self.status})"
