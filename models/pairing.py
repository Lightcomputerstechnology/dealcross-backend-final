from tortoise.models import Model
from tortoise import fields
class Pairing(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField("models.User", related_name="pairings", on_delete=fields.CASCADE)
    counterparty = fields.ForeignKeyField("models.User", related_name="paired_with", on_delete=fields.CASCADE)
    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)
