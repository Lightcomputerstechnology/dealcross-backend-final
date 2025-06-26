# File: models/admin.py

from fastapi_admin.models import AbstractAdmin
from tortoise import fields

class Admin(AbstractAdmin):
    name = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=50, default="admin")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin(id={self.id}, username='{self.username}')"