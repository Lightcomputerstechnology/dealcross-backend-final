from tortoise import fields, models

class RolePermission(models.Model):
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=100, unique=True)
    permissions = fields.JSONField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "role_permission"

    def __str__(self):
        return self.role_name