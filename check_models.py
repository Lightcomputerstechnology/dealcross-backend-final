import asyncio
from tortoise import Tortoise
from core.config import TORTOISE_ORM

async def check_models():
    print("🔍 Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    print("✅ Models loaded successfully!\n")

    relations = []
    for name, model in Tortoise.apps["models"].items():
        for f in model._meta.fk_fields:
            fk_model = model._meta.fields_map[f].related_model
            relations.append((model._meta.table, fk_model._meta.table))

    print("🔗 Foreign Key Relations:")
    for a, b in relations:
        print(f"  {a}  ->  {b}")

    # Detect cycles
    graph = {}
    for a, b in relations:
        graph.setdefault(a, []).append(b)

    visited = set()
    path = []

    def dfs(node):
        if node in path:
            print("⚠️ Cycle detected:", " → ".join(path + [node]))
            return True
        if node in visited:
            return False
        path.append(node)
        visited.add(node)
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        path.pop()
        return False

    print("\n🔍 Checking for cycles...\n")
    for node in graph:
        if dfs(node):
            break
    else:
        print("✅ No cycles detected!")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_models())
