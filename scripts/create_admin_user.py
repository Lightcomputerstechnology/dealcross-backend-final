# scripts/create_admin_user.py

import asyncio
from tortoise import Tortoise
from models.admin import Admin
from core.security import get_password_hash
from project_config.dealcross_config import settings

async def init():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()

async def create_admin_user():
    email = input("Enter admin email (default: admin@dealcross.net): ") or "admin@dealcross.net"
    username = input("Enter admin username (default: admin): ") or "admin"
    password = input("Enter admin password: ")
    if not password:
        print("❌ Password cannot be empty.")
        return

    hashed_password = get_password_hash(password)

    existing = await Admin.get_or_none(email=email)
    if existing:
        print(f"⚠️ Admin with email {email} already exists.")
    else:
        admin = await Admin.create(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True
        )
        print(f"✅ Admin user created successfully: {admin.email}")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())
    asyncio.run(create_admin_user())