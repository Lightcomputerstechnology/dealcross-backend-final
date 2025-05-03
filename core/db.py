# File: core/db.py

from tortoise import Tortoise

# Initialize Tortoise ORM
async def init_db():
    await Tortoise.init(
        db_url="postgresql://dealcross_db_mybg_user:uaDD6kKDRWuESF6YCnvaWvJjGQkUymDl@dpg-d06rhgali9vc73elmnlg-a/dealcross_db_mybg",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()

# Close DB connections gracefully
async def close_db():
    await Tortoise.close_connections()

# Aerich configuration for migrations
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
                "models.chat",  # ✅ Included Chat model
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}
