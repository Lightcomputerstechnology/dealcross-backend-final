#!/bin/bash

export PYTHONPATH=/opt/render/project/src

echo "=== Running smart Aerich migration check ==="

# Safety: Show Python & pip versions
python --version
pip --version

# Safety: Forcefully uninstall deprecated aioredis if still present
pip uninstall -y aioredis || echo "aioredis not found or already removed"

# Check if aerich.ini exists
if [ -f "aerich.ini" ]; then
  echo "Found aerich.ini"

  # Try to run upgrade — only if migrations folder exists
  if [ -d "migrations/models" ]; then
    echo "Found migrations, attempting upgrade..."
    aerich upgrade || echo "Aerich upgrade failed or not needed"
  else
    echo "No migrations found. Skipping aerich upgrade."
  fi
else
  echo "No aerich.ini file found. Skipping Aerich migration."
fi

# Start FastAPI app
echo "Starting FastAPI..."
exec uvicorn main:app --host=0.0.0.0 --port=8000