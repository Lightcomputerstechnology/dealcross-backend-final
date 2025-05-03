# core/database.py

from tortoise import Tortoise
from config import settings  # Your Pydantic settings file

# Get DATABASE URL from .env or settings
DATABASE_URL = settings.DATABASE_URL

# === Aerich-Compatible ORM Config ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # Include aerich models
            "default_connection": "default",
        }
    }
}

# === Initialize Tortoise ORM ===
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["models"]},
    )
    # ❌ Removed: await Tortoise.generate_schemas() — now using Aerich

# === Graceful DB Close ===
async def close_db():
    await Tortoise.close_connections()