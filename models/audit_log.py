from tortoise.models import Model
from tortoise import fields

class AuditLog(Model):
    id = fields.IntField(pk=True)
    action = fields.CharField(max_length=255)

    performed_by = fields.ForeignKeyField(
        "models.User",
        related_name="audit_log_entries",  # ✅ unique and descriptive
        on_delete=fields.CASCADE
    )

    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "audit_logs"

    def __str__(self):
        return f"AuditLog(action={self.action}, performed_by={self.performed_by_id})"