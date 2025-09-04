#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=.

echo "=== Dealcross Boot ==="

# Clean stale bytecode
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Optional: ensure old aioredis isn't present (you use redis.asyncio)
pip uninstall -y aioredis >/dev/null 2>&1 || true

# Run DB migrations (upgrade only; no init/migrate in prod)
if [ -f "aerich.ini" ]; then
  echo "Running aerich upgrade…"
  aerich upgrade || echo "aerich already up-to-date."
else
  echo "No aerich.ini found. Skipping migrations."
fi

# Respect provider PORT, default to 10000 locally
PORT="${PORT:-10000}"
echo "Starting uvicorn on :${PORT}"
exec uvicorn main:app --host 0.0.0.0 --port "${PORT}"
