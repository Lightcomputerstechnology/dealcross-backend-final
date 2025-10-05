import asyncio
from tortoise import Tortoise
from core.config import TORTOISE_ORM
from collections import defaultdict

async def check_models():
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    print("\n✅ Models loaded successfully!\n")

    edges = []

    # Loop through all models and collect foreign key relationships
    for name, model in Tortoise.apps["models"].items():
        table_name = model._meta.db_table  # ✅ Use db_table instead of .table
        for f in model._meta.fk_fields:
            fk_model = model._meta.fields_map[f].related_model
            fk_table = fk_model._meta.db_table
            edges.append((table_name, fk_table))
            print(f"{table_name}  ->  {fk_table}")

    print("\n🔍 Checking for cycles...\n")

    # Build dependency graph
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)

    # Detect cycles using DFS
    def has_cycle():
        visited, rec_stack = set(), set()

        def dfs(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True
            rec_stack.remove(node)
            return False

        return any(dfs(node) for node in graph)

    if has_cycle():
        print("⚠️ Cyclic FK reference detected!")
    else:
        print("✅ No cycles found! Safe schema.")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_models())
