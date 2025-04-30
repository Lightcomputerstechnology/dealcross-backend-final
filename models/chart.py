# File: models/chart.py

# File: models/chat.py

from tortoise import fields
from tortoise.models import Model

class ChatMessage(Model):
    id = fields.IntField(pk=True)
    
    sender = fields.ForeignKeyField(
        "models.User", related_name="sent_messages", on_delete=fields.CASCADE
    )
    receiver = fields.ForeignKeyField(
        "models.User", related_name="received_messages", on_delete=fields.CASCADE
    )
    
    deal = fields.ForeignKeyField(
        "models.Deal", related_name="chat_messages", null=True, on_delete=fields.SET_NULL
    )
    
    content = fields.TextField()
    is_read = fields.BooleanField(default=False)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"
        ordering = ["timestamp"]

    def __str__(self):
        return f"[{self.timestamp}] {self.sender_id} → {self.receiver_id}: {self.content[:20]}"