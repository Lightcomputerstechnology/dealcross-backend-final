from tortoise.models import Model
from tortoise import fields

class AdminWallet(Model):
    id = fields.IntField(pk=True)
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = fields.DatetimeField(auto_now=True)
