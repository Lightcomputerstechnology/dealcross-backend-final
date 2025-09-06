"""
Central Tortoise ORM config.

- Loads settings from project_config/dealcross_config.py
- Lists ONLY existing model modules.
- Keeps Aerich’s internal model at the end.
"""

from project_config.dealcross_config import settings

TORTOISE_ORM = {
    "connections": {
        "default": settings.get_effective_database_url(),
    },
    "apps": {
        "models": {
            "models": [
                # ---- Core / Auth / Admin ----
                "models.user",
                "models.admin",
                "models.audit",       # ✅ your audit.py
                "models.audit_log",   # ✅ your audit_log.py

                # ---- Wallet & Platform earnings ----
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.platform_earnings",
                "models.admin_wallet",
                "models.admin_wallet_log",

                # ---- Deals / Disputes ----
                "models.deal",             # contains Deal, EscrowTracker, Pairing
                "models.dispute",
                "models.pending_approval",

                # ---- KYC ----
                "models.kyc",

                # ---- Messaging / Referrals / Fraud / Charts ----
                "models.chat",
                "models.referral_reward",
                "models.fraud",
                "models.chart",

                # ---- Aerich internal model (must be included) ----
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}