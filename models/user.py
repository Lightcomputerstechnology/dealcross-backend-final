# File: models/user.py

from enum import Enum
from tortoise import models, fields

# User roles enum
class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

# User model
class User(models.Model):
    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    full_name = fields.CharField(max_length=255, null=True)

    role = fields.CharEnumField(UserRole, default=UserRole.user)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    status = fields.CharField(max_length=20, default="active")
    cumulative_sales = fields.DecimalField(max_digits=12, decimal_places=2, default=0)

    hashed_password = fields.CharField(max_length=128)

    referral_code = fields.CharField(max_length=20, unique=True, null=True)
    referred_by = fields.ForeignKeyField(
        "models.User",
        related_name="referrals",
        null=True,
        on_delete=fields.SET_NULL
    )

    permission = fields.ForeignKeyField(
        "models.RolePermission",
        null=True,
        related_name="users",
        on_delete=fields.SET_NULL
    )

    # 2FA fields
    is_2fa_enabled = fields.BooleanField(default=False)
    two_fa_method = fields.CharField(max_length=10, null=True)  # e.g., "totp", "email"
    two_fa_secret = fields.CharField(max_length=64, null=True)  # TOTP secret

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user"  # ✅ matches your live migration
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.username} ({self.email})"