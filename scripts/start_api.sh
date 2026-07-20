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

PORT="$(normalize_port "${1:-${IKP_API_PORT:-8000}}")"
HOST="${IKP_API_HOST:-127.0.0.1}"
UI_PORT="$(normalize_port "${IKP_UI_PORT:-5173}")"
LOG_FILE="${IKP_API_LOG:-api_server.log}"
PID_FILE="${IKP_API_PID_FILE:-.api_pid}"

cors_origins=(
    "http://localhost:${UI_PORT}"
    "http://127.0.0.1:${UI_PORT}"
)

if [[ -n "${IKP_UI_PUBLIC_HOST:-}" ]]; then
    cors_origins+=("http://${IKP_UI_PUBLIC_HOST}:${UI_PORT}")
fi

CORS_ALLOWED_ORIGINS="${CORS_ALLOWED_ORIGINS:-$(IFS=,; echo "${cors_origins[*]}")}"

echo "Starting FastAPI server on ${HOST}:${PORT}..."

# Kill any existing process on this port
if command -v lsof >/dev/null 2>&1 && lsof -Pi ":${PORT}" -sTCP:LISTEN -t >/dev/null ; then
    echo "Killing existing process on port ${PORT}..."
    kill $(lsof -Pi ":${PORT}" -sTCP:LISTEN -t) || true
fi

# Start the server in the background. `nohup` keeps it alive after this
# helper script exits in terminals/agent shells that send SIGHUP to jobs.
nohup env CORS_ALLOWED_ORIGINS="${CORS_ALLOWED_ORIGINS}" \
    uv run --python 3.11 uvicorn ikp_platform.api:app --host "${HOST}" --port "${PORT}" \
    > "${LOG_FILE}" 2>&1 < /dev/null &
API_PID=$!

echo "Waiting for server to be healthy..."
max_retries=30
count=0
while ! curl -fs "http://127.0.0.1:${PORT}/api/status" > /dev/null 2>&1; do
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo "Server failed to start in time. Check ${LOG_FILE}"
        kill "${API_PID}" || true
        exit 1
    fi
    sleep 1
done

echo "Server is UP and healthy at http://127.0.0.1:${PORT}/api (PID: ${API_PID})"
echo "${API_PID}" > "${PID_FILE}"

if [[ "${1:-}" == "--foreground" || "${2:-}" == "--foreground" ]]; then
    echo "Running in foreground mode. Press Ctrl+C to stop."
    wait "${API_PID}"
fi
