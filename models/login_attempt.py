from tortoise.models import Model
from tortoise import fields
class LoginAttempt(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="login_attempts", on_delete=fields.CASCADE)
    ip_address = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now_add=True)
    successful = fields.BooleanField()
