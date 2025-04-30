# File: models/chart.py

from tortoise.models import Model
from tortoise import fields

class ChartPoint(Model):
    """
    Represents a single data point on an admin chart (e.g., user growth, revenue).
    """
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=100, index=True)  # Indexed for filtering
    value = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chart_points"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"<ChartPoint {self.label} = {self.value} @ {self.timestamp}>"