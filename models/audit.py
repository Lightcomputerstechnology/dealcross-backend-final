from tortoise import fields, models

# ─────────── AUDIT LOGS MODEL ───────────

class AuditRecord(models.Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()  # Flexible length

    performed_by = fields.ForeignKeyField(
        "models.user.User",  # Fully qualified path: app_name.ModelName
        related_name="audit_logs",
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "audit_logs"  # Clear table name for DB

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:20]}...')"