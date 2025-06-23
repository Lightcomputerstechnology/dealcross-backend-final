from tortoise import fields
from tortoise.models import Model

class Notification(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.user.User",  # ✅ Correct module path
        related_name="notifications",
        on_delete=fields.CASCADE
    )

    title = fields.CharField(max_length=255, null=True)
    message = fields.TextField()
    is_read = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification(to={self.user_id}, read={self.is_read})"