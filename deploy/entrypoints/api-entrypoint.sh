#!/bin/sh

set -e
cd /app

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

echo "[FASTAPI]: Running..."
uvicorn src.main:app --host="0.0.0.0" --port="${INNER_API_PORT}" --workers="${API_WORKERS_AMOUNT}"