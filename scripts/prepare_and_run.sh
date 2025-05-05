#!/bin/bash

echo "=== Running smart Aerich migration check ==="

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

# Finally start the app
echo "Starting FastAPI..."
exec uvicorn main:app --host=0.0.0.0 --port=8000