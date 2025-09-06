# File: core/database.py
from tortoise import Tortoise
from project_config.dealcross_config import settings
import logging

logger = logging.getLogger("dealcross.db")

DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "models",          # auto-discover your exported models
                "aerich.models",   # keep aerich metadata registered
            ],
            "default_connection": "default",
        }
    },
}

async def init_db():
    logger.info("🔌 Initializing Tortoise ORM…")
    # IMPORTANT: do NOT call generate_schemas here.
    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("✅ Tortoise ORM initialized successfully.")

async def close_db():
    try:
        await Tortoise.close_connections()
        logger.info("✅ Tortoise connections closed successfully.")
    except Exception as e:
        logger.error("❌ Failed to close Tortoise connections: %s", e)