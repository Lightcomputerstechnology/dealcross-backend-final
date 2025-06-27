# File: core/database.py

from tortoise import Tortoise
from config import settings  # Load DATABASE_URL and other settings from .env

async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models"]}  # ✅ This will auto-discover models if __init__.py imports are set
    )
    # await Tortoise.generate_schemas()  # ❌ Skip if using Aerich migrations for consistency

async def close_db():
    await Tortoise.close_connections()