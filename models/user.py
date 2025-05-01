from tortoise import Model, fields
import enum

# ─────────── USER ROLES ENUM ───────────

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

# ─────────── USER MODEL ───────────

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True, null=False)
    email = fields.CharField(max_length=255, unique=True, null=False)
    password = fields.CharField(max_length=255, null=False)
    role = fields.CharEnumField(UserRole, default=UserRole.user)
    email_verified = fields.BooleanField(default=False)  # ✅ Added field
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"User({self.username}, {self.email}, {self.role})"