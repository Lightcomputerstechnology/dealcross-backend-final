# File: models/webhook.py

from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class WebhookLog(Model):
    id = fields.IntField(pk=True)
    source = fields.CharField(max_length=100, index=True)  # e.g., "Stripe", "Flutterwave"
    event_type = fields.CharField(max_length=100)
    payload = fields.JSONField()
    received_at = fields.DatetimeField(default=datetime.utcnow)
    processed = fields.BooleanField(default=False)
    status_message = fields.TextField(null=True)
    tag = fields.CharField(max_length=50, null=True, index=True)  # Optional: e.g., deal, user, kyc
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "webhook_logs"
        ordering = ["-received_at"]

    def __str__(self):
        return f"{self.source} [{self.event_type}] @ {self.received_at.strftime('%Y-%m-%d %H:%M')}"