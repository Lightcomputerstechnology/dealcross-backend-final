from tortoise.models import Model
from tortoise import fields
class Config(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255, unique=True)
    value = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
