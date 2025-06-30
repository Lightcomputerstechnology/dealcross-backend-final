from tortoise import fields, models

class RolePermission(models.Model):
    """
    RolePermission links roles to permissions in the system.
    Extend as needed with your business logic.
    """
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=100)
    permission_name = fields.CharField(max_length=100)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "role_permissions"

    def __str__(self):
        return f"{self.role_name} - {self.permission_name}"