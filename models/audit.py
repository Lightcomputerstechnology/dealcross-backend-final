from tortoise import models, fields

# ─────────── AUDIT LOG MODEL ───────────

class Audit(models.Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()

    performed_by = fields.ForeignKeyField(
        "models.User",  # ✅ Correct Tortoise format: "app.Model"
        related_name="audit_logs",
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "audit_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:30]}...')"