import asyncio
from tortoise import Tortoise
from core.config import TORTOISE_ORM
from collections import defaultdict


async def check_models():
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    print("\n✅ Models loaded successfully!\n")

    edges = []

    # Collect all foreign key relationships
    for name, model in Tortoise.apps["models"].items():
        for f in model._meta.fk_fields:
            fk_model = model._meta.fields_map[f].related_model._meta.db_table
            edges.append((model._meta.db_table, fk_model))
            print(f"{model._meta.db_table}  ->  {fk_model}")

    print("\n🔍 Checking for cycles...\n")

    # Build adjacency list
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)

    # Depth-first cycle detection
    def has_cycle():
        visited, rec = set(), set()

        def dfs(node):
            if node in rec:
                return True
            if node in visited:
                return False
            visited.add(node)
            rec.add(node)
            for n in graph[node]:
                if dfs(n):
                    return True
            rec.remove(node)
            return False

        return any(dfs(n) for n in list(graph))

    if has_cycle():
        print("🚨 Cyclic FK reference detected!")
    else:
        print("✅ No cycles found! Safe schema.")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_models())
