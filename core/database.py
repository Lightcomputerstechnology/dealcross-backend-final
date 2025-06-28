# core/database.py

from tortoise import Tortoise
from config.settings import settings  # ✅ explicitly from config.settings

DATABASE_URL = settings.get_effective_database_url()

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