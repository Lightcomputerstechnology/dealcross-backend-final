# File: models/support.py

from tortoise import fields, models
from tortoise.models import Model
from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class SupportTicket(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True, index=True)
    subject = fields.CharField(max_length=255)
    message = fields.TextField()
    status = fields.CharEnumField(TicketStatus, default=TicketStatus.OPEN)
    priority = fields.CharEnumField(TicketPriority, default=TicketPriority.MEDIUM)
    tags = fields.CharField(max_length=100, null=True)
    read_by_admin = fields.BooleanField(default=False)
    attachment = fields.CharField(max_length=255, null=True)
    admin_response = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "support_tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.priority}] {self.subject[:40]} (#{self.id})"