# core/config.py

"""
Central Tortoise ORM config.
- Reuses the single settings source in project_config/dealcross_config.py
- Explicitly lists model modules so Aerich can detect them for migrations.
"""

from project_config.dealcross_config import settings

TORTOISE_ORM = {
    "connections": {
        # Ensure 'postgresql://' is converted to 'postgres://' inside settings
        "default": settings.get_effective_database_url(),
    },
    "apps": {
        "models": {
            "models": [
                # ---- List ALL model modules explicitly ----
                "models.user",
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.deal",
                "models.dispute",
                "models.kyc",
                "models.chat",
                "models.admin_wallet",
                "models.admin_wallet_log",
                "models.platform_earnings",
                "models.referral_reward",
                "models.auditlog",
                "models.chart",

                # Aerich internal model (must be last or included)
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}