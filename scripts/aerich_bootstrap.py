import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AERICH_INI = REPO_ROOT / "aerich.ini"
MIGRATIONS_DIR = REPO_ROOT / "migrations"
MODELS_INIT = MIGRATIONS_DIR / "models" / "__init__.py"

def run(cmd: str) -> int:
    print(f"▶ {cmd}")
    return subprocess.call(cmd, shell=True)

def main():
    # Ensure we're running from the repo root so aerich sees aerich.ini
    os.chdir(REPO_ROOT)
    print(f"ℹ Working dir: {Path.cwd()}")

    # 1) Validate aerich.ini
    if not AERICH_INI.exists():
        print("❌ aerich.ini missing at repo root — create it first.")
        sys.exit(2)
    else:
        print("✅ Found aerich.ini")

    # 2) First run vs upgrade
    if MIGRATIONS_DIR.is_dir() and MODELS_INIT.exists():
        print("🔼 Running `aerich upgrade`...")
        code = run("aerich upgrade")
        if code != 0:
            print("⚠ aerich upgrade failed or already up-to-date. Continuing...")
    else:
        print("🆕 First run: initializing Aerich…")
        # NOTE: core.config.TORTOISE_ORM must point at your explicit model list
        run("aerich init -t core.config.TORTOISE_ORM || true")
        code = run("aerich init-db")
        if code != 0:
            print("❌ aerich init-db failed.")
            sys.exit(code)

    print("✅ Aerich bootstrap finished.")
    return 0

if __name__ == "__main__":
    sys.exit(main())