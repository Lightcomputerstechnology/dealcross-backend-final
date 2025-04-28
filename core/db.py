# File: core/db.py

from tortoise import Tortoise
from config import settings  # ✅ Use your existing Pydantic settings

# Initialize Tortoise ORM
async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,  # ✅ Pull DATABASE_URL from settings
        modules={"models": ["models"]}  # ✅ Points to your models directory
    )
    await Tortoise.generate_schemas()  # Optional: Auto-create tables (skip if using Aerich)

# Close DB connections gracefully
async def close_db():
    await Tortoise.close_connections()

# Aerich config dictionary
TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
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
                "aerich.models"  # Include Aerich models
            ],
            "default_connection": "default",
        }
    },
}