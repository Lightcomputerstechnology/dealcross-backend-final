# File: models/fee_transaction.py

from enum import Enum
from tortoise import models, fields
from decimal import Decimal

# Transaction Status Enum
class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

# Transaction Type Enum
class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    fee = "fee"
    adjustment = "adjustment"

# FeeTransaction Model
class FeeTransaction(models.Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",  # ✅ correct reference
        related_name="fee_transactions",
        on_delete=fields.CASCADE
    )

    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    currency = fields.CharField(max_length=10, default="USD")

    transaction_type = fields.CharEnumField(TransactionType)
    status = fields.CharEnumField(TransactionStatus, default=TransactionStatus.pending)

    description = fields.TextField(null=True)

    reference = fields.CharField(max_length=100, unique=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "fee_transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"FeeTransaction {self.id} | User {self.user_id} | "
            f"{self.amount} {self.currency} | {self.status}"
        )