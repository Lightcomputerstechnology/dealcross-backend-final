# File: core/database.py

from tortoise import Tortoise
from project_config.dealcross_config import settings

DATABASE_URL = settings.database_url

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
    """
    Initialize the Tortoise ORM on startup.

    🚫 Do NOT use generate_schemas() in production as it causes cyclic FK conflicts.
    ✅ Use Aerich to handle migrations safely.
    """
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        print("✅ Tortoise ORM initialized successfully.")
    except Exception as e:
        print("❌ Tortoise ORM initialization failed:", e)


async def close_db():
    """
    Close all Tortoise ORM connections gracefully on shutdown.
    """
    try:
        await Tortoise.close_connections()
        print("✅ Tortoise connections closed successfully.")
    except Exception as e:
        print("❌ Failed to close Tortoise connections:", e)
