from models.user import User
from core.security import get_password_hash

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "Admin@123"  # ⚠️ Change in production
DEFAULT_ADMIN_EMAIL = "admin@dealcross.net"

async def seed_default_admin():
    existing = await User.get_or_none(username=DEFAULT_ADMIN_USERNAME)
    if not existing:
        await User.create(
            username=DEFAULT_ADMIN_USERNAME,
            email=DEFAULT_ADMIN_EMAIL,
            hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
            is_active=True,
            is_superuser=True,
            full_name="Dealcross Admin"
        )
        print("✅ Default admin user created.")
    else:
        print("ℹ️ Default admin user already exists.")