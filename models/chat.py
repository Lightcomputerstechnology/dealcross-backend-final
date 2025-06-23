from tortoise import fields
from tortoise.models import Model

class ChartPoint(Model):
    id = fields.IntField(pk=True)
    label = fields.CharField(max_length=100)
    value = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chart_points"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.label}: {self.value}"