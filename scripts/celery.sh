# scripts/start_celery.sh  ★ solo + 재시작
#!/usr/bin/env bash
set -euo pipefail
#source .venv/bin/activate
CELERY_OPTS=(
  -A tasks.asodesign worker
  --pool=solo
  --concurrency=1
  --max-tasks-per-child=1
  --loglevel=info
)
while true; do
  echo "[ℹ] Celery worker (solo) starting…"
  exec celery "${CELERY_OPTS[@]}"
  echo "[⚠] Celery worker exited – restarting in 2s…"
  sleep 2
done
