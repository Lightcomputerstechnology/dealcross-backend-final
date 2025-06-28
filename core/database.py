# core/database.py

from tortoise import Tortoise
from config import settings  # from your config/settings.py

# ✅ Use the effective_database_url property correctly
DATABASE_URL = settings.effective_database_url  # Uses DATABASE_URL or builds from parts

# === Aerich-Compatible ORM Config ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # Correct for Tortoise + Aerich
            "default_connection": "default",
        }
    }
}

# === Initialize Tortoise ORM ===
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    # await Tortoise.generate_schemas()  # ❌ Use Aerich for migrations instead

# === Graceful DB Close ===
async def close_db():
    await Tortoise.close_connections()