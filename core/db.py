# File: core/db.py

import os
from tortoise import Tortoise

# Grab your Render DATABASE_URL (must start with postgres://)
DB_URL = os.getenv("DATABASE_URL")

# Dynamic init for FastAPI
async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()

# Graceful shutdown
async def close_db():
    await Tortoise.close_connections()

# Static config for Aerich (migrations)
# You can call os.getenv here at import‑time—it just has to be postgres://
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL
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
                "models.chat",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
