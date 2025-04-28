from tortoise.models import Model
from tortoise import fields
class ChartPoint(Model):
    id = fields.IntField(pk=True)
    value = fields.FloatField()
    label = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now_add=True)
