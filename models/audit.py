from tortoise import fields, models

class Audit(models.Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()  # Flexible length

    performed_by = fields.ForeignKeyField(
        "models.User",  # ✅ Use app.Model format, assuming 'models' is your Tortoise app label
        related_name="audit_logs",
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "audit_logs"  # ✅ Optional but clearer for DB naming

    def __str__(self):
        return f"Audit(id={self.id}, action='{self.action[:20]}...')"