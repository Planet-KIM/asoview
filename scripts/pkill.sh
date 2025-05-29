# scripts/stop_all.sh
#!/usr/bin/env bash
set +e
pkill -f gunicorn
pkill -f manage.py
pkill -f 'celery.*worker'
pkill -x redis-server
echo "[⏹] Services stopped"