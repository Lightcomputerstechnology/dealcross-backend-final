from tortoise import Tortoise
from core.config import TORTOISE_ORM
import asyncio
from collections import defaultdict


async def check_models():
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    print("\nModels loaded successfully!\n")

    edges = []
    for name, model in Tortoise.apps["models"].items():
        for f in model._meta.fk_fields:
            fk_model = model._meta.fields_map[f].related_model._meta.table
            edges.append((model._meta.table, fk_model))
            print(f"{model._meta.table}  ->  {fk_model}")

    print("\nChecking for cycles...\n")

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)

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
        print("⚠️ Cyclic FK reference detected!")
    else:
        print("✅ No cycles found! Safe schema.")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_models())
