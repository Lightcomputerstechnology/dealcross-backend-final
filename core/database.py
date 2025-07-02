# File: core/database.py

from tortoise import Tortoise
from core.settings import settings

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
    Temporarily generate schemas to create missing tables like 'admins'.
    Remove the schema generation line after confirming admin login works.
    """
    await Tortoise.init(config=TORTOISE_ORM)

    # ⚠️ TEMPORARY:
    # This will auto-create missing tables like 'admins' during your first deploy.
    # ✅ REMOVE AFTER confirming admin login works to avoid conflicts in production.
    try:
        await Tortoise.generate_schemas()
        print("✅ Tortoise schemas generated successfully (tables created if missing).")
    except Exception as e:
        print("❌ Schema generation failed:", e)

async def close_db():
    """
    Close all Tortoise ORM connections gracefully on shutdown.
    """
    await Tortoise.close_connections()
