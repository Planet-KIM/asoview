# scripts/start_redis.sh
#!/usr/bin/env bash
# 포그라운드로 띄우면 터미널 고정되므로 --daemonize yes 사용
if command -v redis-server >/dev/null 2>&1; then
  redis-server --daemonize yes
  echo "[✔] redis-server started (port 6379)"
else
  echo "[✖] redis-server 명령을 찾을 수 없습니다.
  • macOS  : brew install redis
  • Ubuntu : sudo apt-get install redis-server" >&2
  exit 1
fi