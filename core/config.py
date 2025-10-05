"""
Central Tortoise ORM config.
Uses project_config/dealcross_config.py for DB URL.
"""

from project_config.dealcross_config import settings

DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                # ✅ Explicitly list all model modules to avoid cyclic imports
                "models.user",
                "models.wallet",
                "models.wallet_transaction",
                "models.admin_wallet",
                "models.admin_wallet_log",
                "models.kyc",
                "models.deal",
                "models.dispute",
                "models.fraud",
                "models.audit",
                "models.audit_log",
                "models.metric",
                "models.chart",
                "models.chat",
                "models.login_attempt",
                "models.platform_earnings",
                "models.referral_reward",
                "models.support",
                "models.share",
                "models.settings",
                "models.pending_approval",
                "models.banner",
                "models.role_permission",
                "models.webhook",
                "models.notification",
                "models.investor_report",
                "models.escrow_tracker",
                "models.fee_transaction",
                "models.pairing",
                "models.blog",
                "models.config",
                "models.logs",
                "models.aiinsight",
                "models.admin",
                "aerich.models",  # ✅ Aerich metadata
            ],
            "default_connection": "default",
        }
    },
}