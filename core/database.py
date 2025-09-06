from __future__ import annotations

import logging
from tortoise import Tortoise
from project_config.dealcross_config import settings

logger = logging.getLogger("dealcross.db")

# Use the effective URL (handles postgresql:// → postgres://)
DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            # IMPORTANT: Use the explicit model module list from core/config.py
            # Do NOT rely on "models" autodiscovery here, to keep things predictable.
            "models": ["aerich.models"],  # placeholder; real list comes from core/config.TORTOISE_ORM
            "default_connection": "default",
        }
    },
}

async def init_db():
    """
    Initialize Tortoise ORM.

    - Do NOT call generate_schemas() here (we let Supabase/Aerich create tables).
    - Do NOT spawn Aerich subprocesses in production (Render free dynos don’t need it).
    """
    try:
        logger.info("🔌 Initializing Tortoise ORM…")
        # NOTE: We import the canonical config from core.config to ensure the
        # model module list is the single source of truth.
        from core.config import TORTOISE_ORM as CANONICAL_ORM
        await Tortoise.init(config=CANONICAL_ORM)
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