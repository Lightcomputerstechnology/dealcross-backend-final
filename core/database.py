from tortoise import Tortoise
from config import settings  # Assumes a config/settings.py using Pydantic

# Load from environment or settings file
DATABASE_URL = settings.DATABASE_URL

# === Aerich-Compatible ORM Config ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.models.__models__", "aerich.models"],  # ✅ Use centralized model list
            "default_connection": "default",
        }
    }
}

# === Initialize Tortoise ORM ===
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["src.models.__models__"]},  # ✅ Must match TORTOISE_ORM config
    )
    # await Tortoise.generate_schemas()  # ❌ Don't use if Aerich handles migrations

# === Graceful DB Close ===
async def close_db():
    await Tortoise.close_connections()
