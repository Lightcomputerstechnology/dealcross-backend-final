from tortoise import Model, fields

# ─────────── USER NOTIFICATION MODEL ───────────

class Notification(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="notifications",
        on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=255, null=True)  # ✅ Optional: add title for better UX
    message = fields.TextField()
    is_read = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification(to={self.user_id}, read={self.is_read})"
