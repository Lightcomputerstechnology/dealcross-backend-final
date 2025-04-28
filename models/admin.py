from tortoise import fields
from tortoise.models import Model

class Admin(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    role = fields.CharField(max_length=255, default="admin")
    created_at = fields.DatetimeField(auto_now_add=True)
