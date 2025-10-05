import asyncio
from tortoise import Tortoise
from project_config.dealcross_config import settings
from models.admin import Admin
from core.security import get_password_hash


async def create_admin():
    # ✅ Dynamically detect correct database URL
    if hasattr(settings, "DATABASE_URL"):
        db_url = settings.DATABASE_URL
    elif hasattr(settings, "get_effective_database_url"):
        db_url = settings.get_effective_database_url()
    elif hasattr(settings, "database_url"):
        db_url = settings.database_url
    else:
        raise AttributeError("⚠️ No valid database URL found in settings")

    # ✅ Initialize ORM
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["models.admin"]},
    )

    email = "admin@dealcross.net"
    password = "ChangeMeSecurely@123"
    hashed_password = get_password_hash(password)

    print("🔍 Checking for existing admin...")
    existing = await Admin.filter(email=email).first()
    if existing:
        print(f"⚠️ Admin with email {email} already exists.")
    else:
        await Admin.create(
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True,
        )
        print(f"✅ Admin created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Temporary Password: {password}")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(create_admin())