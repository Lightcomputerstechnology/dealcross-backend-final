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
                "models.fee_transaction",         # ✅ Fee tracking
                "models.admin_wallet",
                "models.admin_wallet_log",        # ✅ Admin logging
                "models.kyc",
                "models.deal",
                "models.dispute",                 # ✅ Optional but important
                "models.fraud",
                "models.audit_log",
                "models.metric",
                "models.chart",
                "models.chat",
                "models.login_attempt",           # ✅ Optional for login monitoring
                "models.platform_earnings",       # ✅ Earnings tracking
                "models.referral_reward",         # ✅ Referral system
                "aerich.models",                  # Required
            ],
            "default_connection": "default",
        }
    },
}