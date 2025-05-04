import os
from tortoise import Tortoise

# Render environment variable
DB_URL = os.getenv("DATABASE_URL")

# Tortoise ORM init for FastAPI
async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": [
            "models.user",
            "models.kyc",
            "models.wallet",
            "models.wallet_transaction",
            "models.fee_transaction",
            "models.admin_wallet",
            "models.admin_wallet_log",
            "models.deal",
            "models.dispute",
            "models.fraud",
            "models.audit_log",
            "models.metric",
            "models.chart",
            "models.chat",
            "models.login_attempt",
            "models.platform_earnings",
            "models.referral_reward",
            "aerich.models"  # Required for migration tracking
        ]}
    )
    # COMMENTED OUT for safety in production:
    # await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()

# Aerich configuration
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL
    },
    "apps": {
        "models": {
            "models": [
                "models.user",
                "models.kyc",
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.admin_wallet",
                "models.admin_wallet_log",
                "models.deal",
                "models.dispute",
                "models.fraud",
                "models.audit_log",
                "models.metric",
                "models.chart",
                "models.chat",
                "models.login_attempt",
                "models.platform_earnings",
                "models.referral_reward",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}