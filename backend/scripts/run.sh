#!/bin/bash
# ------------------------------------------------------------------------------
# Intellex AI Backend Startup & Verification Utility Script
# ------------------------------------------------------------------------------

set -e

echo "=== [Intellex AI Backend Utility] ==="

# 1. Verify environment file exists
if [ ! -f .env ]; then
    echo "⚠️ .env file not found! Copying from .env.example..."
    cp .env.example .env
fi

# 2. Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✅ Activating local virtual environment (venv)..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✅ Activating local virtual environment (.venv)..."
    source .venv/bin/activate
fi

# 3. Check Python and dependencies
echo "🔍 Checking Python and pip dependencies..."
python3 -m pip install -r requirements.txt

# 4. Apply migrations if a PostgreSQL database is reachable
echo "🔄 Checking database connection and running migrations..."
alembic upgrade head || echo "⚠️ Migration step skipped or database is not reachable. Ensure PostgreSQL is active."

# 5. Start Uvicorn Server
echo "🚀 Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
