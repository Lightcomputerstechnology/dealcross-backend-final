"""
Central Tortoise ORM config.

- Loads settings from project_config/dealcross_config.py
- Explicitly lists ALL model modules that exist in your /models folder
  so Aerich can detect them reliably (no implicit discovery).
"""

from project_config.dealcross_config import settings

TORTOISE_ORM = {
    "connections": {
        # Make sure postgresql:// is converted to postgres:// inside settings
        "default": settings.get_effective_database_url(),
    },
    "apps": {
        "models": {
            "models": [
                # ---- Core auth / users / roles ----
                "models.user",
                "models.role",
                "models.role_permission",
                "models.login_attempt",

                # ---- Admin & audit ----
                "models.admin",
                "models.audit",          # audit model(s)
                "models.audit_log",      # audit log entries

                # ---- Wallet & fees / platform ----
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.platform_earnings",
                "models.admin_wallet",
                "models.admin_wallet_log",

                # ---- Deals / escrow / disputes / pairing / approvals ----
                "models.deal",
                "models.escrow_tracker",
                "models.dispute",
                "models.pairing",
                "models.pending_approval",

                # ---- KYC ----
                "models.kyc",
                "models.kyc_request",

                # ---- Referrals ----
                "models.referral_reward",

                # ---- Notifications / support ----
                "models.notification",
                "models.support",

                # ---- Content / reporting / misc ----
                "models.blog",
                "models.banner",
                "models.investor_report",
                "models.share",
                "models.chart",
                "models.metric",
                "models.webhook",
                "models.config",         # project settings stored in DB
                "models.settings",       # (exists in your repo)
                "models.fraud",
                "models.chat",
                "models.logs",           # generic logs
                "models.aiinsight",      # AI insight module

                # ---- Aerich internal model (required) ----
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}