import os
from tortoise import Tortoise

DB_URL = os.getenv("DATABASE_URL")

# Tortoise ORM init for FastAPI
async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["src.models.__models__"]}  # ✅ Centralized model loader
    )
    # await Tortoise.generate_schemas()  # Optional: Enable for first-time dev use only

async def close_db():
    await Tortoise.close_connections()

# Aerich-compatible config
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL
    },
    "apps": {
        "models": {
            "models": ["src.models.__models__", "aerich.models"],  # ✅ Unified model loader + aerich
            "default_connection": "default",
        }
    }
}
