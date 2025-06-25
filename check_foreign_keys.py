import os
import ast
from termcolor import colored

MODELS_DIR = "models"
EXPECTED_PREFIX = "models."

def is_foreign_key_call(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "ForeignKeyField"
    )

def extract_foreign_key_model(node):
    if not node.args:
        return None
    arg = node.args[0]
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    return None

def scan_models():
    issues = []
    for root, _, files in os.walk(MODELS_DIR):
        for file in files:
            if not file.endswith(".py") or file.startswith("__"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read(), filename=file)
                except SyntaxError as e:
                    print(colored(f"[SYNTAX ERROR] {file}: {e}", "red"))
                    continue

            for node in ast.walk(tree):
                if is_foreign_key_call(node):
                    ref = extract_foreign_key_model(node)
                    if ref and not ref.startswith(EXPECTED_PREFIX):
                        issues.append((file, ref))
    return issues

if __name__ == "__main__":
    print(colored("🔍 Checking ForeignKeyField references...\n", "cyan", attrs=["bold"]))
    problems = scan_models()

    if problems:
        for file, value in problems:
            print(colored(f"❌ {file}", "yellow"), f"has invalid ForeignKeyField:", colored(f'"{value}"', "red"))
        print(colored("\n⚠️ Fix all ForeignKeyField references to follow this format: \"models.ModelName\"\n", "magenta"))
    else:
        print(colored("✅ All ForeignKeyField references are valid!\n", "green"))