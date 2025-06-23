from tortoise import Model, fields

# ─────────── AUDIT LOGS MODEL ───────────

class Audit(Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()  # Flexible length
    performed_by = fields.ForeignKeyField(
        "models.User",  # ✅ Correct format
        related_name="audit_logs",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:20]}...')"