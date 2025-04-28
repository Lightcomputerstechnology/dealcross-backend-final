from tortoise import fields, models

# ─────────── ADMIN MODEL ───────────

class Admin(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    role = fields.CharField(max_length=50, default="admin")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin(id={self.id}, email='{self.email}')"
