"""
Central Tortoise ORM config.

- Loads settings from project_config/dealcross_config.py
- Lists ONLY model modules that actually exist right now.
- Keeps Aerich’s internal model at the end.
"""

from project_config.dealcross_config import settings

TORTOISE_ORM = {
    "connections": {
        # settings.get_effective_database_url() converts postgresql:// → postgres:// for Tortoise
        "default": settings.get_effective_database_url(),
    },
    "apps": {
        "models": {
            "models": [
                # ---- Core / Auth / Admin ----
                "models.user",
                "models.admin",            # you shared this file
                "models.auditlog",         # earlier code referenced 'models.auditlog'

                # ---- Wallet & Platform earnings ----
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.platform_earnings",
                "models.admin_wallet",
                "models.admin_wallet_log",

                # ---- Deals / Disputes ----
                "models.deal",             # currently also contains EscrowTracker & Pairing classes
                # DO NOT include "models.escrow_tracker" or "models.pairing"
                # unless you have split them into separate files.

                "models.dispute",
                "models.pending_approval", # you shared this file

                # ---- KYC ----
                "models.kyc",              # keep this (you referenced it across routers)

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