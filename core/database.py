# File: core/database.py

from tortoise import Tortoise
from config.settings import settings  # ✅ Ensure this is correct

DATABASE_URL = settings.database_url  # ✅ This will now work

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    }
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

async def close_db():
    await Tortoise.close_connections()