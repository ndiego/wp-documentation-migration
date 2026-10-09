#!/bin/bash
# Starts Playground server detached, waits until PHP answers (200 or auto-login 302), prints boot time.
# Usage: ./start-server.sh [extra cli flags...]
cd "$(dirname "$0")"
pkill -f "wp-playground-cli server" 2>/dev/null; while pgrep -f "wp-playground-cli server" >/dev/null; do perl -e 'select(undef,undef,undef,0.2)'; done
T0=$(perl -MTime::HiRes=time -e 'printf "%.3f", time')
nohup ./node_modules/.bin/wp-playground-cli server --blueprint=${BLUEPRINT:-blueprint.json} --blueprint-may-read-adjacent-files --port=9400 "$@" > server.log 2>&1 &
PID=$!
for i in $(seq 1 1200); do
  c=$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9400/wp-login.php || true)
  if [ "$c" = 200 ] || [ "$c" = 302 ]; then break; fi
  if ! kill -0 $PID 2>/dev/null; then echo "SERVER DIED"; tail -20 server.log; exit 1; fi
  perl -e 'select(undef,undef,undef,0.25)'
done
T1=$(perl -MTime::HiRes=time -e 'printf "%.3f", time')
echo "first-response=$c boot_seconds=$(echo "$T1 - $T0" | bc)"
