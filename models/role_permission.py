# File: models/role_permission.py
from tortoise import models, fields

class RolePermission(models.Model):
    """
    Single source of truth for role/permission mapping.
    Example rows:
      ("admin", "users.manage")
      ("admin", "deals.approve")
      ("user",  "deals.create")
    """
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=100)         # e.g. "admin", "user"
    permission_name = fields.CharField(max_length=100)   # e.g. "users.manage"
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "role_permissions"
        unique_together = (("role_name", "permission_name"),)

    def __str__(self) -> str:
        return f"{self.role_name} - {self.permission_name}"
