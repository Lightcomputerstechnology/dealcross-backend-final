from tortoise import Model, fields

# ─────────── AUDIT LOGS MODEL ───────────

class Audit(Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()  # Upgraded for flexibility (longer actions)
    performed_by = fields.ForeignKeyField(
        "models.User", related_name="audit_logs", on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:20]}...')"
