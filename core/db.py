# File: core/db.py

from tortoise import Tortoise
from config import settings

# Initialize Tortoise ORM
async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models"]}  # Automatically detects all listed models
    )
    await Tortoise.generate_schemas()

# Close DB connections gracefully
async def close_db():
    await Tortoise.close_connections()

# Aerich configuration for migrations
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "models.user",
                "models.wallet",
                "models.wallet_transaction",
                "models.admin_wallet",
                "models.kyc",
                "models.deal",
                "models.fraud",
                "models.audit_log",
                "models.metric",
                "models.chart",
                "models.chat",        # ✅ Included Chat model
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}