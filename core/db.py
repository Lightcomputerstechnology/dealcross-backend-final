# File: core/db.py

import os
from tortoise import Tortoise

# Normalize Render DB URL
def normalize_db_url(raw_url: str) -> str:
    if raw_url and raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql://", 1)
    return raw_url

# Initialize Tortoise ORM
async def init_db():
    db_url = normalize_db_url(os.getenv("DATABASE_URL"))
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()

# Close DB connections gracefully
async def close_db():
    await Tortoise.close_connections()

# Aerich configuration for migrations
db_url_env = normalize_db_url(os.getenv("DATABASE_URL"))

TORTOISE_ORM = {
    "connections": {
        "default": db_url_env
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
                "models.chat",  # ✅ Included Chat model
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}
