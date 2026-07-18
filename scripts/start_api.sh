#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-8000}
echo "Starting FastAPI server on port $PORT..."

# Kill any existing process on this port
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "Killing existing process on port $PORT..."
    kill -9 $(lsof -Pi :$PORT -sTCP:LISTEN -t)
fi

# Start the server in the background
uv run --python 3.11 python -m ikp_platform.api > mcp_server.log 2>&1 &
API_PID=$!

echo "Waiting for server to be healthy..."
max_retries=30
count=0
while ! curl -s "http://localhost:$PORT/api/status" > /dev/null; do
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo "Server failed to start in time. Check mcp_server.log"
        kill $API_PID
        exit 1
    fi
    sleep 1
done

echo "Server is UP and healthy! (PID: $API_PID)"
echo $API_PID > .api_pid
