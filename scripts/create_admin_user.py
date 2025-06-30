# File: scripts/create_admin_user.py

import asyncio
from models.admin import Admin
from core.security import get_password_hash

async def create_admin():
    username = "admin"
    email = "admin@dealcross.net"
    password = "StrongPassword123"

    hashed_password = get_password_hash(password)

    admin = await Admin.create(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_superuser=True,
        is_active=True
    )
    print(f"✅ Admin created: {admin.email}")

if __name__ == "__main__":
    asyncio.run(create_admin())