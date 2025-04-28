from tortoise import Model, fields

# ─────────── DISPUTE MODEL ───────────

class Dispute(Model):
    id = fields.IntField(pk=True)
    deal = fields.ForeignKeyField(
        "models.Deal",
        related_name="disputes",
        on_delete=fields.CASCADE
    )
    reason = fields.CharField(max_length=255)
    details = fields.TextField()
    status = fields.CharField(max_length=50, default="open")  # Optimized size for status field
    created_at = fields.DatetimeField(auto_now_add=True)
    resolved_at = fields.DatetimeField(null=True)

    def __str__(self):
        return f"Dispute(deal_id={self.deal_id}, status={self.status})"
