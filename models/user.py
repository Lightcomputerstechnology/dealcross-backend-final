# models/user.py
from enum import Enum
from tortoise import Model, fields

class UserRole(str, Enum):
    user      = "user"
    moderator = "moderator"
    auditor   = "auditor"
    admin     = "admin"

class User(Model):
    id               = fields.IntField(pk=True)
    username         = fields.CharField(max_length=50, unique=True)
    email            = fields.CharField(max_length=255, unique=True)
    full_name        = fields.CharField(max_length=255, null=True)
    role             = fields.CharEnumField(UserRole, default=UserRole.user)
    status           = fields.CharField(max_length=20, default="active")
    cumulative_sales = fields.DecimalField(max_digits=12, decimal_places=2, default=0)
    hashed_password  = fields.CharField(max_length=128)
    referral_code    = fields.CharField(max_length=20, unique=True, null=True)
    referred_by      = fields.ForeignKeyField(
        "models.User",
        related_name="referrals",
        null=True,
        on_delete=fields.SET_NULL
    )
    created_at       = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
        
