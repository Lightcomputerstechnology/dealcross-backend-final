from tortoise import fields
from tortoise.models import Model

class ChatMessage(Model):
    id = fields.IntField(pk=True)

    sender = fields.ForeignKeyField(
        "models.user.User",  # ✅ Correct ForeignKey reference
        related_name="sent_messages",
        on_delete=fields.CASCADE
    )

    receiver = fields.ForeignKeyField(
        "models.user.User",  # ✅ Correct ForeignKey reference
        related_name="received_messages",
        on_delete=fields.CASCADE
    )

    message = fields.TextField()
    is_read = fields.BooleanField(default=False)
    sent_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"From {self.sender_id} to {self.receiver_id}"