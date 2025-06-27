# File: models/admin.py

from tortoise import models, fields

class Admin(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)  # Used for login
    hashed_password = fields.CharField(max_length=255)     # Used for login
    name = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=50, default="admin")
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admins"

    def __str__(self):
        return f"Admin(id={self.id}, email='{self.email}')"