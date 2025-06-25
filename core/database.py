from tortoise import Tortoise
from config import settings  # from your config/settings.py

# Use Pydantic settings to load env vars
DATABASE_URL = settings.DATABASE_URL

# === Aerich-Compatible ORM Config ===
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # ✅ NO "src." — must match Tortoise label!
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