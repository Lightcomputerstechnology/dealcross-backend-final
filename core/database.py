# core/database.py

from tortoise import Tortoise
from config import settings

# Correct: call the method, not attribute
DATABASE_URL = settings.get_effective_database_url()

# Aerich-compatible config
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