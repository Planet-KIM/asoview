#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/../.venv/bin/activate"

# 1) Redis 실행
pgrep -x redis-server >/dev/null || "$DIR/redis.sh"

# 2) Celery 백그라운드
"$DIR/celery.sh" >>"$DIR/../logs/celery.log" 2>&1 &
CELERY_PID=$!

# 3) Gunicorn
mkdir -p "$DIR/../logs"
PORT=${1:-5000}
gunicorn -w 2 -b 0.0.0.0:"$PORT" wsgi:app \
  >>"$DIR/../logs/gunicorn.log" 2>&1 &
GUNICORN_PID=$!

echo "[✓] API at http://localhost:$PORT (Gunicorn PID $GUNICORN_PID)"
trap 'echo "\n[⏹] Stopping…"; kill $GUNICORN_PID $CELERY_PID; pkill -x redis-server; exit 0' INT
wait