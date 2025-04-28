from tortoise import Tortoise
from config import settings  # Your Pydantic settings

# Tortoise ORM config using DATABASE_URL and SSL
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL  # uses postgresql+asyncpg://
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
                "aerich.models"  # Required for migrations
            ],
            "default_connection": "default",
        }
    },
}
