# File: models/fee_transaction.py

from enum import Enum
from tortoise import models, fields

class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    fee = "fee"
    adjustment = "adjustment"

class FeeTransaction(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="fee_transactions",