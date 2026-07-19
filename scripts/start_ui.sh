#!/usr/bin/env bash
set -euo pipefail

normalize_port() {
    local raw="$1"
    if [[ "${raw}" =~ ^1[0-9]{4}$ ]]; then
        echo "${raw:1}"
    else
        echo "${raw}"
    fi
}

PORT="$(normalize_port "${1:-${IKP_UI_PORT:-5173}}")"
API_PORT="$(normalize_port "${2:-${IKP_API_PORT:-8000}}")"
HOST="${IKP_UI_HOST:-127.0.0.1}"
API_PUBLIC_HOST="${IKP_API_PUBLIC_HOST:-localhost}"
API_BASE_URL="${VITE_API_BASE_URL:-http://${API_PUBLIC_HOST}:${API_PORT}/api}"
LOG_FILE="${IKP_UI_LOG:-ui_server.log}"
PID_FILE="${IKP_UI_PID_FILE:-.ui_pid}"

echo "Starting Vite UI on ${HOST}:${PORT}..."
echo "Using API base URL: ${API_BASE_URL}"

cd ikp_web

# Kill any existing process on this port
if command -v lsof >/dev/null 2>&1 && lsof -Pi ":${PORT}" -sTCP:LISTEN -t >/dev/null ; then
    echo "Killing existing process on port ${PORT}..."
    kill $(lsof -Pi ":${PORT}" -sTCP:LISTEN -t) || true
fi

# Start the UI in the background. `nohup` keeps it alive after this helper
# script exits in terminals/agent shells that send SIGHUP to jobs.
nohup env VITE_API_BASE_URL="${API_BASE_URL}" \
    npm run dev -- --port "${PORT}" --host "${HOST}" \
    > "../${LOG_FILE}" 2>&1 < /dev/null &
UI_PID=$!

echo "Waiting for UI server to be accessible..."
max_retries=30
count=0
while ! curl -fs "http://127.0.0.1:${PORT}" > /dev/null 2>&1; do
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo "UI server failed to start in time. Check ${LOG_FILE}"
        kill "${UI_PID}" || true
        exit 1
    fi
    sleep 1
done

echo "UI Server is UP at http://127.0.0.1:${PORT} (PID: ${UI_PID})"
echo "${UI_PID}" > "../${PID_FILE}"
