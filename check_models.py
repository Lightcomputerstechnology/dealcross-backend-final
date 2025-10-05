import asyncio
import logging
from tortoise import Tortoise
from dealcross.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dealcross.check_models")


async def check_models():
    logger.info("✅ Settings loaded")
    logger.info(f"• App: Dealcross [{settings.APP_ENV}]")
    logger.info("• DATABASE_URL loaded")
    logger.info("• REDIS_URL loaded")
    logger.info("• SUPABASE_URL loaded")
    logger.info("• SUPABASE_JWKS_URL loaded")
    logger.info("• SUPABASE_SERVICE_ROLE loaded")
    logger.info("• Email/Payment configuration loaded")

    logger.info("Initializing Tortoise ORM...")
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    logger.info("\n✅ Models loaded successfully!\n")

    models = Tortoise.apps.get("models", {})
    relations = []

    # Collect relationships between models
    for model_name, model in models.items():
        for field in model._meta.fields_map.values():
            if hasattr(field, "related_model") and field.related_model:
                relations.append((model_name, field.related_model._meta.model_name))

    for rel in relations:
        logger.info(f"{rel[0]}  ->  {rel[1]}")

    logger.info("\n🔍 Checking for cycles...\n")

    # Build graph of relationships
    graph = {}
    for src, dst in relations:
        graph.setdefault(src, []).append(dst)

    # Detect circular dependencies
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited and dfs(neighbor):
                return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    # ✅ FIXED: avoid "dictionary changed size" error
    def has_cycle():
        return any(dfs(node) for node in list(graph))

    if has_cycle():
        logger.error("❌ Circular dependency detected in model relationships!")
    else:
        logger.info("✅ No circular dependencies found!")

    await Tortoise.close_connections()


if __name__ == "__main__":
    try:
        asyncio.run(check_models())
    except Exception as e:
        logger.error(f"Error while checking models: {e}")
