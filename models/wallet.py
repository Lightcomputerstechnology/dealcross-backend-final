from tortoise import fields
from tortoise.models import Model

class Wallet(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="wallet", on_delete=fields.CASCADE)
    balance = fields.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "wallet"  # Ensure the table name matches your database structure