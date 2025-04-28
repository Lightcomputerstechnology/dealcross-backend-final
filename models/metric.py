# File: src/models/metric.py

from tortoise.models import Model
from tortoise import fields

class Metric(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=100, index=True)  # Example: "users", "deals", "wallets_funded"
    value = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "metrics"

    def __str__(self):
        return f"Metric(type={self.type}, value={self.value})"
