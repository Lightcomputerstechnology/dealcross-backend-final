# File: core/database.py

from tortoise import Tortoise
from config import settings  # Ensure this path is correct for your project

# Correct direct retrieval
DATABASE_URL = settings.database_url

# === Aerich-Compatible ORM Config ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # must match your Tortoise/Aerich config
            "default_connection": "default",
        }
    }
}

# === Initialize Tortoise ORM ===
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    # Use Aerich for migrations, do not call generate_schemas here in production

# === Graceful DB Close ===
async def close_db():
    await Tortoise.close_connections()