#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-5173}
echo "Starting Vite UI on port $PORT..."

cd ikp_web

# Kill any existing process on this port
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "Killing existing process on port $PORT..."
    kill -9 $(lsof -Pi :$PORT -sTCP:LISTEN -t)
fi

# Start the UI in the background
npm run dev -- --port $PORT > ../ui_server.log 2>&1 &
UI_PID=$!

echo "Waiting for UI server to be accessible..."
max_retries=30
count=0
while ! curl -s "http://localhost:$PORT" > /dev/null; do
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo "UI server failed to start in time. Check ui_server.log"
        kill $UI_PID
        exit 1
    fi
    sleep 1
done

echo "UI Server is UP and accessible! (PID: $UI_PID)"
echo $UI_PID > ../.ui_pid
