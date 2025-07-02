import asyncio
from tortoise import Tortoise
from project_config.dealcross_config import settings

async def init_admin_table():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models.admin"]},  # ✅ only the admin model
    )
    await Tortoise.generate_schemas()
    print("✅ 'admins' table created successfully.")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init_admin_table())
