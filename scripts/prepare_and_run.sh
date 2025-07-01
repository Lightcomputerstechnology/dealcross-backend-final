#!/bin/bash

set -e  # Exit immediately on any error

export PYTHONPATH=.

echo "=== 🚀 Starting Dealcross Smart Boot Script ==="

# Show environment info for debug
python --version
pip --version

# Clean .pyc and __pycache__ to avoid stale bytecode issues
echo "🧹 Cleaning .pyc and __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Force uninstall deprecated aioredis if present
echo "🩹 Checking and removing deprecated aioredis if present..."
pip uninstall -y aioredis || echo "✅ aioredis not found or already removed."

# Run Aerich migrations smartly
echo "🛠️ Running Aerich migration steps..."

# Check for aerich.ini presence
if [ -f "aerich.ini" ]; then
    echo "✅ Found aerich.ini"

    # Run `aerich init` if migrations folder is missing
    if [ ! -d "migrations/models" ]; then
        echo "📂 Migrations folder not found, initializing Aerich..."
        aerich init -t core.config.TORTOISE_ORM || echo "✅ Aerich init already done."
        aerich init-db || echo "✅ Aerich init-db already done or schema already exists."
    else
        echo "✅ Migrations folder found, skipping init."
    fi

    # Run migrations
    echo "⚙️ Attempting Aerich upgrade..."
    aerich upgrade || echo "✅ Aerich upgrade failed or already up-to-date."

else
    echo "⚠️ No aerich.ini found. Skipping Aerich migrations."
fi

# Show critical environment variables for verification
echo "✅ Environment variables in use:"
env | grep -E 'DATABASE_URL|DB_|REDIS_URL|JWT_SECRET|APP_ENV|PORT'

# Determine port to use (Render/Heroku use $PORT, fallback to 10000)
PORT=${PORT:-10000}

echo "🚀 Starting FastAPI app on port ${PORT}..."
uvicorn main:app --host 0.0.0.0 --port "${PORT}"