# seed_admin.py

import asyncio
from tortoise import Tortoise
from core.settings import settings
from models.admin import Admin
from core.security import get_password_hash

async def create_admin():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models"]},
    )

    email = "admin@dealcross.net"
    password = "ChangeMeSecurely@123"
    hashed_password = get_password_hash(password)

    existing = await Admin.filter(email=email).first()
    if existing:
        print(f"⚠️ Admin with email {email} already exists.")
    else:
        await Admin.create(
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True
        )
        print(f"✅ Admin created: {email} with password: {password}")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(create_admin())
