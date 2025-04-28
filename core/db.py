from tortoise import Tortoise
from config import settings  # Your Pydantic settings

# Tortoise ORM config using DATABASE_URL and SSL
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "uri": settings.DATABASE_URL,  # Use the full URL from settings
                "ssl": True                    # Enable SSL here
            }
        }
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
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}

# Initialize Tortoise
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

# Close connection
async def close_db():
    await Tortoise.close_connections()
