from tortoise import Tortoise
from config import settings  # ✅ Use your existing pydantic settings

async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,  # ✅ Pull DATABASE_URL from settings
        modules={"models": ["models"]}  # ✅ Tells Tortoise where your models live
    )
    await Tortoise.generate_schemas()  # Optional: Auto-create tables (skip if using Aerich)

async def close_db():
    await Tortoise.close_connections()