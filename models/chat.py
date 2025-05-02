# models/chat.py

from tortoise import fields
from tortoise.models import Model

class ChatMessage(Model):
    """
    Represents a message exchanged between two users, optionally tied to a specific deal.
    """
    id = fields.IntField(pk=True)

    sender = fields.ForeignKeyField("models.User", related_name="sent_messages", on_delete=fields.CASCADE)
    receiver = fields.ForeignKeyField("models.User", related_name="received_messages", on_delete=fields.CASCADE)
    deal = fields.ForeignKeyField("models.Deal", related_name="chat_messages", null=True, on_delete=fields.SET_NULL)

    message = fields.TextField()
    is_read = fields.BooleanField(default=False)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
        ordering = ["timestamp"]

    def __str__(self):
        return f"[{self.timestamp}] {self.sender_id} → {self.receiver_id}: {self.message[:30]}"

    def __repr__(self):
        return f"<ChatMessage #{self.id} from {self.sender_id} to {self.receiver_id}>"
