# File: scripts/create_admin_user.py

import asyncio
from models.admin import Admin
from passlib.hash import bcrypt
import sys

async def create_admin():
    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()

    existing = await Admin.get_or_none(email=email)
    if existing:
        print(f"Admin with email '{email}' already exists.")
        return

    hashed_password = bcrypt.hash(password)
    admin = await Admin.create(email=email, hashed_password=hashed_password, is_superuser=True)
    print(f"✅ Admin user created with ID {admin.id} and email {admin.email}")

if __name__ == "__main__":
    try:
        asyncio.run(create_admin())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)