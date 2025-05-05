models/webhook.py

from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class WebhookLog(Model):
    id = fields.IntField(pk=True)
    source = fields.CharField(max_length=100)  # e.g., "Stripe", "Flutterwave"
    event_type = fields.CharField(max_length=100)
    payload = fields.JSONField()
    received_at = fields.DatetimeField(default=datetime.utcnow)
    processed = fields.BooleanField(default=False)
    status_message = fields.TextField(null=True)

    class Meta:
        table = "webhook_logs"
        ordering = ["-received_at"]

    def __str__(self):
        return f"Webhook from {self.source} at {self.received_at}"

