"""
Central Tortoise ORM config.

- Pulls settings from project_config/dealcross_config.py
- Explicitly lists ALL model modules in your repo so Aerich can detect them.
  (If a module doesn't define a Tortoise model, it won't break anything.)
"""

from project_config.dealcross_config import settings

TORTOISE_ORM = {
    "connections": {
        # Ensures postgresql:// → postgres:// for Tortoise
        "default": settings.get_effective_database_url(),
    },
    "apps": {
        "models": {
            "models": [
                # ---- Core users/roles/permissions ----
                "models.user",
                "models.role",
                "models.role_permission",
                "models.login_attempt",

                # ---- Admin & audit ----
                "models.admin",                # ✅ your Admin table
                "models.audit",               # (if this defines models)
                "models.audit_log",           # audit logs

                # ---- Wallet & fees/earnings ----
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
                "models.config",              # project settings in DB (if used)
                "models.settings",            # if this also defines models
                "models.fraud",
                "models.chat",
                "models.logs",                # generic logs
                "models.aiinsight",           # your AI insight module

                # ---- Aerich internal model (required) ----
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}