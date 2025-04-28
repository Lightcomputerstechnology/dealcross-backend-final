from tortoise import Tortoise
from config import settings  # Your Pydantic settings

# Tortoise ORM config using DATABASE_URL and SSL
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "dpg-d06rhgali9vc73elmnlg-a",
                "port": 5432,
                "user": "dealcross_db_mybg_user",
                "password": "uaDD6kKDRWuESF6YCnvaWvJjGQkUymDl",
                "database": "dealcross_db_mybg",
                "ssl": True  # ✅ This handles SSL for asyncpg!
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
