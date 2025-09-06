from __future__ import annotations
import os
import logging
from tortoise import Tortoise
from project_config.dealcross_config import settings

logger = logging.getLogger("dealcross.db")

# Pull the effective connection string (handles postgresql:// → postgres://)
DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "models",          # auto-discover models/
                "aerich.models",   # aerich’s internal
            ],
            "default_connection": "default",
        }
    }
}

# Toggle automatic schema creation (on by default for free Render)
AUTO_SCHEMA = os.getenv("AUTO_SCHEMA", "1")  # "1" = enabled, "0" = disabled


async def init_db():
    """
    Initialize Tortoise ORM.

    - On free hosting (no shell): AUTO_SCHEMA=1 → auto-create tables if missing.
    - On paid hosting (with shell): set AUTO_SCHEMA=0 and run `aerich upgrade` instead.
    """
    try:
        logger.info("🔌 Initializing Tortoise ORM...")
        await Tortoise.init(config=TORTOISE_ORM)

        if AUTO_SCHEMA in ("1", "true", "True", "yes", "on"):
            logger.info("🛠️ AUTO_SCHEMA enabled → generating schemas safely.")
            await Tortoise.generate_schemas(safe=True)
            logger.info("✅ Schemas verified/created (safe mode).")
        else:
            logger.info("ℹ️ AUTO_SCHEMA disabled. Skipping schema generation.")

        logger.info("✅ Tortoise ORM initialized successfully.")
    except Exception as e:
        logger.error("❌ Tortoise ORM initialization failed: %s", e)
        raise


async def close_db():
    """Close all Tortoise ORM connections gracefully."""
    try:
        await Tortoise.close_connections()
        logger.info("✅ Tortoise connections closed successfully.")
    except Exception as e:
        logger.error("❌ Failed to close Tortoise connections: %s", e)