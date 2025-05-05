# File: models/pending_approval.py

from tortoise import fields, models
from models.user import User

class PendingApproval(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="pending_requests")
    request_type = fields.CharField(max_length=100)  # e.g. "kyc", "deal", "update"
    details = fields.TextField()
    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_type} - {self.status}"