# File: scripts/create_admin_user.py

import asyncio
from tortoise import Tortoise
from models.admin import Admin
from passlib.hash import bcrypt
from project_config.dealcross_config import settings

async def create_admin():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models"]}
    )
    # Optional: generate schemas if needed for first-time use
    # await Tortoise.generate_schemas()

    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()

    existing = await Admin.get_or_none(email=email)
    if existing:
        print(f"Admin with email '{email}' already exists.")
        await Tortoise.close_connections()
        return

    hashed_password = bcrypt.hash(password)
    admin = await Admin.create(email=email, hashed_password=hashed_password, is_superuser=True)
    print(f"✅ Admin user created with ID {admin.id} and email {admin.email}")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(create_admin())