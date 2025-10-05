import os
import sys
import asyncio
import logging
from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError

# --------------------------------------------------------------------------
# ✅ Ensure the project root is on the Python path
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# --------------------------------------------------------------------------
# ✅ Load your settings properly from the existing config
# --------------------------------------------------------------------------
try:
    from project_config.dealcross_config import settings
    logging.info("✅ Settings loaded successfully from project_config.dealcross_config")
except ModuleNotFoundError as e:
    logging.error(f"❌ Could not import settings: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("check_models")

# --------------------------------------------------------------------------
# ✅ Main function to initialize and verify models
# --------------------------------------------------------------------------
async def check_models():
    logger.info("Initializing Tortoise ORM...")

    try:
        await Tortoise.init(
            db_url=settings.DATABASE_URL,
            modules={
                "models": [
                    "models.user",
                    "models.wallets",
                    "models.deals",
                    "models.transactions",
                    "models.admin_wallet",
                    "models.kyc",
                    "models.audit",
                    "models.support",
                    "models.chat",
                    "models.notification",
                    "models.pending_approvals",
                    "models.pairings",
                    "models.platform_earnings",
                ]
            },
        )
        logger.info("✅ Models loaded successfully!")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error while initializing ORM: {e}")
        sys.exit(1)

    # ----------------------------------------------------------------------
    # ✅ Build relationship graph for cycle detection
    # ----------------------------------------------------------------------
    models = Tortoise.apps.get("models").values()
    relations = []
    for model in models:
        for fk_field in model._meta.fk_fields:
            fk_model = model._meta.fields_map[fk_field].related_model
            relations.append((model._meta.db_table, fk_model._meta.db_table))

    logger.info("\nDetected relationships (foreign keys):")
    for a, b in relations:
        logger.info(f"{a}  ->  {b}")

    # ----------------------------------------------------------------------
    # ✅ Check for cyclic dependencies (causes Aerich “cyclic fk” error)
    # ----------------------------------------------------------------------
    logger.info("\n🔍 Checking for cyclic foreign key references...")

    graph = {}
    for a, b in relations:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set())

    visited = set()
    rec_stack = set()

    def dfs(node):
        if node not in visited:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited and dfs(neighbor):
                    return True
                elif neighbor in rec_stack:
                    return True
        rec_stack.remove(node)
        return False

    has_cycle = any(dfs(n) for n in list(graph.keys()))

    if has_cycle:
        logger.error("❌ Cycle detected in model foreign key relationships!")
    else:
        logger.info("✅ No cycles detected — schema creation should work fine!")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_models())
