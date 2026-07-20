#!/usr/bin/env bash
set -euo pipefail

PID_FILE="${IKP_UI_PID_FILE:-.ui_pid}"
PORT="${1:-${IKP_UI_PORT:-5173}}"

cd ikp_web || exit 1

if [[ -f "../${PID_FILE}" ]]; then
    UI_PID=$(cat "../${PID_FILE}")
    if kill -0 "${UI_PID}" 2>/dev/null; then
        echo "Stopping UI server (PID: ${UI_PID})..."
        kill -TERM "${UI_PID}"
        rm -f "../${PID_FILE}"
        echo "UI server stopped."
        exit 0
    else
        echo "UI server PID file exists but process is not running. Cleaning up PID file."
        rm -f "../${PID_FILE}"
    fi
fi

# Fallback using lsof
if command -v lsof >/dev/null 2>&1 && lsof -Pi ":${PORT}" -sTCP:LISTEN -t >/dev/null ; then
    FALLBACK_PID=$(lsof -Pi ":${PORT}" -sTCP:LISTEN -t | head -n 1)
    echo "Stopping UI server on port ${PORT} (PID: ${FALLBACK_PID})..."
    kill -TERM "${FALLBACK_PID}"
    echo "UI server stopped."
else
    echo "No UI server found running on port ${PORT} or PID file."
fi
