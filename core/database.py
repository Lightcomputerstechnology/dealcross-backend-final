# File: core/database.py

from tortoise import Tortoise
from project_config.dealcross_config import settings  # ✅ Consistent, correct import

# ✅ Use the lowercase attribute which now works
DATABASE_URL = settings.database_url

# === Tortoise ORM Configuration (Aerich Compatible) ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # ✅ Always match your models + aerich
            "default_connection": "default",
        }
    }
}

# === Initialize Tortoise ORM ===
async def init_db():
    """
    Initialize the Tortoise ORM on startup.
    Do not generate schemas here if using Aerich for migrations.
    """
    await Tortoise.init(config=TORTOISE_ORM)

# === Close Tortoise Connections on Shutdown ===
async def close_db():
    """
    Close all Tortoise ORM connections gracefully on shutdown.
    """
    await Tortoise.close_connections()
