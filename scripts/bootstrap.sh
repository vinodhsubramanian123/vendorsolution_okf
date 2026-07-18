#!/usr/bin/env bash
# Seeds the local `repository/` folder from the PDFs in sources/pdfs/.
#
# `repository/` is intentionally gitignored (it's a generated artifact,
# not source of truth) -- so this MUST be run once after cloning, and
# again any time sources/pdfs/ changes, before starting the API.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "No .env found -- copying .env.example. Edit it and set GEMINI_API_KEY" >&2
  echo "before re-running, or ingestion will proceed without LLM-assisted" >&2
  echo "rule extraction / semantic indexing (both degrade gracefully)." >&2
  cp .env.example .env
fi

echo "Ingesting sources/pdfs/ into repository/ ..."
uv run python -m ikp_platform.scripts.ingest_catalog

echo
echo "Building semantic search index (requires GEMINI_API_KEY) ..."
uv run python -m ikp_platform.scripts.reindex

echo
echo "Done. Check LOG.md for a per-file summary, and needs_review/ for any"
echo "documents that could not be auto-ingested."
