# models/audit.py

from tortoise import fields, models

class Audit(models.Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()  # Flexible length

    performed_by = fields.ForeignKeyField(
        "models.User",  # ✅ Correct Tortoise format: "app.Model"
        related_name="audit_logs",
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "audit_logs"  # Optional, but good for clarity

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:20]}...')"