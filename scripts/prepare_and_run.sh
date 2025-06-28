#!/bin/bash

set -e  # Exit immediately on error

export PYTHONPATH=.

echo "=== Running smart Aerich migration check ==="

# Show environment info for debug
python --version
pip --version

# Clean .pyc and __pycache__ to avoid stale bytecode issues
echo "Cleaning .pyc and __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Force uninstall deprecated aioredis if present
pip uninstall -y aioredis || echo "aioredis not found or already removed"

# Run Aerich migrations if configured
if [ -f "aerich.ini" ]; then
    echo "Found aerich.ini"
    if [ -d "migrations/models" ]; then
        echo "Found migrations, attempting Aerich upgrade..."
        aerich upgrade || echo "Aerich upgrade failed or already up-to-date"
    else
        echo "No migrations folder found. Skipping Aerich upgrade."
    fi
else
    echo "No aerich.ini file found. Skipping Aerich migration."
fi

# Final confirmation before boot
echo "Environment variables in use:"
env | grep -E 'DATABASE_URL|DB_|REDIS_URL|SECRET_KEY|APP_ENV'

# Start FastAPI app on port 10000
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 10000