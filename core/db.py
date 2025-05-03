# File: core/db.py

import os
from tortoise import Tortoise

# Normalize the DB URL
def normalize_db_url(raw_url: str) -> str:
    if raw_url and raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql://", 1)
    return raw_url

# Dynamic init for FastAPI
async def init_db():
    db_url = normalize_db_url(os.getenv("DATABASE_URL"))
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()

# Graceful shutdown
async def close_db():
    await Tortoise.close_connections()

# Static config for Aerich (MUST use postgresql:// here directly)
TORTOISE_ORM = {
    "connections": {
        "default": "postgresql://dealcross_db_mybg_user:uaDD6kKDRWuESF6YCnvaWvJjGQkUymDl@dpg-d06rhgali9vc73elmnlg-a/dealcross_db_mybg"
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
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}
