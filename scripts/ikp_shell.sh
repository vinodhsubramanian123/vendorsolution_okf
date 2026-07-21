#!/bin/bash
# IKP Development Shell Environment
# Source this file to activate the environment and load helper functions.
# Usage: source scripts/ikp_shell.sh

source .venv/bin/activate

alias ingest="python3 -m ikp_platform.scripts.ingest_catalog"
alias reindex="python3 -m ikp_platform.scripts.reindex_vector_store"
alias start_api="bash scripts/start_api.sh 8000 --foreground"
alias start_ui="bash scripts/start_ui.sh --foreground"

echo "===================================================="
echo "IKP Development Environment Activated!"
echo "Available commands:"
echo "  ingest     - Run the canonical catalog ingestion"
echo "  reindex    - Reindex the vector store from the graph"
echo "  start_api  - Start the backend FastAPI server"
echo "  start_ui   - Start the frontend React server"
echo "===================================================="
