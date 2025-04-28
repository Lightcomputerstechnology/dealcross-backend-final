# File: src/models/chart.py

from tortoise.models import Model
from tortoise import fields

class ChartPoint(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=100)  # Example: "User Growth", "Revenue"
    value = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chart_points"

    def __str__(self):
        return f"ChartPoint(label={self.label}, value={self.value})"
