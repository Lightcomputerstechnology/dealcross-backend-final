"""
check_models.py
Verifies that all Tortoise ORM models load correctly and checks for cyclic foreign key references.
"""

import asyncio
import logging
from tortoise import Tortoise
from project_config.dealcross_config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("check_models")

async def check_models():
    logger.info("✅ Settings loaded successfully from project_config.dealcross_config")
    logger.info("Initializing Tortoise ORM...")

    # 🔧 Detect correct database URL dynamically
    if hasattr(settings, "DATABASE_URL"):
        db_url = settings.DATABASE_URL
    elif hasattr(settings, "get_effective_database_url"):
        db_url = settings.get_effective_database_url()
    elif hasattr(settings, "database_url"):
        db_url = settings.database_url
    else:
        raise AttributeError("⚠️ Settings object has no database URL defined")

    # ✅ Initialize Tortoise ORM
    try:
        await Tortoise.init(
            db_url=db_url,
            modules={
                "models": [
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
                    "aerich.models",
                ]
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error while initializing ORM: {e}")
        return

    # ✅ Load all models
    models = list(Tortoise.apps.get("models", {}).values())
    logger.info("✅ Models loaded successfully!\n")

    # 🔍 Collect relationships
    relations = []
    for model in models:
        for field_name, field in model._meta.fields_map.items():
            if hasattr(field, "related_model") and field.related_model:
                relations.append((model._meta.db_table, field.related_model._meta.db_table))
                print(f"{model._meta.db_table}  ->  {field.related_model._meta.db_table}")

    print("\n🔍 Checking for cycles...\n")

    # Build dependency graph
    graph = {}
    for a, b in relations:
        graph.setdefault(a, set()).add(b)

    # DFS-based cycle detection
    visited = set()
    stack = set()

    def dfs(node):
        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited and dfs(neighbor):
                return True
            elif neighbor in stack:
                return True
        stack.remove(node)
        return False

    has_cycle = any(dfs(node) for node in list(graph))

    if has_cycle:
        print("❌ Cyclic foreign key reference(s) detected!")
    else:
        print("✅ No cycles found! Safe schema.")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_models())