from tortoise import fields, models
from tortoise.models import Model


class RolePermission(Model):
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True)

    permissions = fields.JSONField(null=True)  # Can store lists like ["view_users", "edit_wallets"]
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Reverse relation: users assigned to this role
    users: fields.ReverseRelation["User"]

    class Meta:
        table = "role_permission"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role_name}"