from tortoise.models import Model
from tortoise import fields
import enum

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    role = fields.CharEnumField(UserRole, default=UserRole.user)
    created_at = fields.DatetimeField(auto_now_add=True)
