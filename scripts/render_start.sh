#!/usr/bin/env bash
set -ueo pipefail

export PYTHONPATH=.

echo "=== Dealcross backend boot ==="
echo "CWD: $(pwd)"
echo "Python: $(python --version)"
echo "Pip:    $(pip --version)"
echo "PORT:   ${PORT:-<unset>}"
echo "ENV:    APP_ENV=${APP_ENV:-}, DATABASE_URL=${DATABASE_URL:-<unset>}, REDIS_URL=${REDIS_URL:-<unset>}"

echo
echo "== Repo tree (top level) =="
ls -la | sed -n '1,200p'

# 1) Ensure aerich.ini exists (Render runs from /opt/render/project/src)
if [[ ! -f aerich.ini ]]; then
  echo "❌ aerich.ini NOT found in repo root. Aborting so you can fix."
  exit 2
fi
echo "✅ aerich.ini found."

# 2) Show aerich.ini so we’re sure the tortoise_orm path is correct
echo
echo "== aerich.ini =="
cat aerich.ini

echo
echo "== Verifying Aerich availability =="
aerich -h >/dev/null 2>&1 && echo "✅ Aerich is installed" || { echo "❌ Aerich not installed"; exit 3; }

# 3) Tortoise ORM settings sanity
python - <<'PY'
from project_config.dealcross_config import settings
from core.config import TORTOISE_ORM
print("✅ settings OK")
print("• Effective DB URL:", settings.get_effective_database_url())
print("• TORTOISE apps:", list(TORTOISE_ORM.get("apps",{})))
print("• Models count:", len(TORTOISE_ORM["apps"]["models"]["models"]))
PY

# 4) Decide between first init and upgrade
echo
if [[ -d migrations && -f migrations/models/__init__.py ]]; then
  echo "🔼 Running 'aerich upgrade' (migrations already present)..."
  aerich upgrade || { echo "❌ aerich upgrade failed"; exit 4; }
else
  echo "🆕 First run: initializing Aerich and DB schema…"
  aerich init -t core.config.TORTOISE_ORM || echo "ℹ️ aerich init already done"
  aerich init-db
fi

echo
echo "🚀 Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-10000}"