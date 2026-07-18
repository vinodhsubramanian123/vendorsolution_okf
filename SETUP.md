# Setup

This is developer setup/run instructions. For the cross-platform
`tools/` PATH-shimming toolchain (`uv run`, `agy`, `graphify`), see
`README.md` and `.agents/rules/toolchain.md` -- that's a different,
complementary doc, not a replacement for this one.

## 1. Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (this project's dependency manifest
  and lockfile are uv-native; see `README.md` for why)
- Node 18+ (for `ikp_web/`, the frontend)
- A Gemini API key (optional but recommended -- see step 3)

## 2. Install

```bash
git clone <this repo>
cd vendorsolution_okf
uv sync --extra dev
```

## 3. Configure environment

```bash
cp .env.example .env
# edit .env and set GEMINI_API_KEY
```

**Note on `GEMINI_API_KEY`:** the platform runs without it. Intent
parsing falls back to keyword heuristics, and PDF ingestion still
extracts structured components/rules/SKUs. What you lose without a
key: LLM-assisted rule extraction from prose, LLM-assisted component
selection, and semantic (vector) search -- those degrade silently to
"no results" rather than erroring, so if search seems to return
nothing, check this first.

## 4. Seed the knowledge repository (required, every fresh clone)

`repository/` -- the canonical OKF markdown files that back the whole
platform -- is **gitignored on purpose** (it's a generated artifact,
not source of truth: the source of truth is `sources/pdfs/` + the
extraction pipeline). This means **a fresh clone has zero knowledge
data** until you run:

```bash
./scripts/bootstrap.sh
```

This reads every PDF in `sources/pdfs/`, extracts platforms /
components / rules / SKUs, and writes them to `repository/`, plus
updates `STATE.md` and `LOG.md` at the project root. Any PDF the
pipeline couldn't confidently parse is written to
`needs_review/<source_id>.json` instead of silently vanishing --
check there if a document you expected isn't in the repository.

Re-run this any time `sources/pdfs/` changes.

## 5. Run the API

```bash
uv run uvicorn ikp_platform.api:app --reload --port 8000
```

If `repository/` wasn't seeded, the API still starts, but logs a
`CRITICAL` warning and every endpoint returns empty results --
`/api/status`'s `repository_seeded` field will be `false`. Run step 4
first.

## 6. Run the frontend

```bash
cd ikp_web
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000/api` by
default; override with `VITE_API_BASE_URL` (see `.env.example`) if
you're running the API elsewhere.

## 7. Run tests

```bash
uv run pytest tests/
```

Tests are fully hermetic -- they run against `tmp_path`-backed fixture
repositories (see `tests/conftest.py`'s `temp_repo` / `api_client`
fixtures), never against the real `repository/`, `STATE.md`, `LOG.md`,
or `CONTEXT.md`. **This has broken three times already** (a hardcoded
`os.getcwd()`-based `RepoManager` call in a test, `test_api_endpoints.py`
importing `api.app` directly, and a scratch debug script committed
into `tests/` that ran at module import time) -- if you're adding a
test that touches `RepoManager`, use the `temp_repo` fixture. Before
trusting a "fix" here again, run the suite 2-3 times in a row and diff
`STATE.md`'s hash; it should never change.

`tests/integration/manual_*.py` and `scripts/debug/*.py` are plain
scripts (`def main()`), not pytest tests -- run them directly with
`uv run python <path>`, not via pytest.

## Project layout

```
ikp_platform/
  api.py                  FastAPI app
  cli.py                  CLI entry point
  mcp_server.py           MCP server entry point
  core/
    ontology/models.py    Pydantic object model (Platform, Component, Rule, ...)
    ingestion/             PDF/Excel -> structured objects
    repository/            OKF markdown <-> in-memory graph, vector index, MCP client
    reasoning/              Intent parsing, rule engine, solution generation, LLM client
    validation/            BOQ / solution validators
  scripts/
    ingest_catalog.py       Batch-ingest sources/pdfs/ -> repository/
    reindex.py               Rebuild the semantic search index (separate from ingestion)
ikp_web/                   React frontend
sources/pdfs/               Source QuickSpecs PDFs
repository/                 GENERATED -- gitignored, run scripts/bootstrap.sh to populate
needs_review/                GENERATED -- documents that failed automated extraction
scripts/debug/               Ad-hoc scratch scripts, not part of any test suite or CI
tests/integration/manual_*.py  Manual end-to-end scripts, not collected by pytest
STATE.md / LOG.md / CONTEXT.md   Generated summaries, updated by RepoManager
IKP/                        Blueprints + agent instructions (not developer docs)
```
