#!/usr/bin/env bash
set -euo pipefail

PID_FILE="${IKP_API_PID_FILE:-.api_pid}"
PORT="${1:-${IKP_API_PORT:-8000}}"

if [[ -f "${PID_FILE}" ]]; then
    API_PID=$(cat "${PID_FILE}")
    if kill -0 "${API_PID}" 2>/dev/null; then
        echo "Stopping API server (PID: ${API_PID})..."
        kill -TERM "${API_PID}"
        rm -f "${PID_FILE}"
        echo "API server stopped."
        exit 0
    else
        echo "API server PID file exists but process is not running. Cleaning up PID file."
        rm -f "${PID_FILE}"
    fi
fi

# Fallback using lsof
if command -v lsof >/dev/null 2>&1 && lsof -Pi ":${PORT}" -sTCP:LISTEN -t >/dev/null ; then
    FALLBACK_PID=$(lsof -Pi ":${PORT}" -sTCP:LISTEN -t | head -n 1)
    echo "Stopping API server on port ${PORT} (PID: ${FALLBACK_PID})..."
    kill -TERM "${FALLBACK_PID}"
    echo "API server stopped."
else
    echo "No API server found running on port ${PORT} or PID file."
fi
