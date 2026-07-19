# 11. Current Implementation Stack

Last reviewed: 2026-07-19

This document reconciles the original IKP/OKF standards with the codebase as it exists now. Standards 01-10 remain the product and architecture intent. When an older standard, generated doc, or agent note conflicts with the current implementation, use this document plus the code as the operational source of truth.

Naming note: the project is `vendorsolution_okf` and the platform is IKP. References to "IKF" are typos unless a future standard explicitly introduces that name.

## Current Runtime

| Layer | Current choice | Notes |
|---|---|---|
| Backend | Python 3.10+ / FastAPI | Main app: `ikp_platform/api.py` |
| Frontend | React / Vite / TypeScript | App folder: `ikp_web/` |
| Workflow | LangGraph | Implemented under `ikp_platform/core/workflow/` |
| Canonical repository | OKF Markdown with YAML frontmatter | Generated under `repository/` by ingestion/bootstrap |
| Graph engine | NetworkX `DiGraph` | Rebuilt in memory from OKF on startup |
| Vector search | ChromaDB local persistent client | Uses Gemini embeddings through `LLMClient` |
| LLM integration | Gemini via `google-genai`; Antigravity CLI for rule mining helpers | Requires `GEMINI_API_KEY` for LLM/embedding quality |
| Ingestion | PDF, Excel, source registry | PDF uses vendor adapters; Excel supports `Components` and `SKUs` sheets |
| Tests | Pytest, Ruff, Vite build, optional Playwright | `mypy` exists as a separate backlog gate |

## How To Run Locally

Default local ports are intentionally simple:

- API: `8000`
- UI: `5173`

Use the scripts so agents do not invent host/port combinations:

```bash
./scripts/start_api.sh
./scripts/start_ui.sh
```

The scripts also accept explicit ports:

```bash
./scripts/start_api.sh 8001
./scripts/start_ui.sh 5174 8001
```

If an agent accidentally passes a five-digit port with a leading `1`, the scripts normalize it for local development. For example, `15173` becomes `5173` and `18000` becomes `8000`.

Useful environment variables:

- `IKP_API_HOST`, default `127.0.0.1`
- `IKP_API_PORT`, default `8000`
- `IKP_UI_HOST`, default `127.0.0.1`
- `IKP_UI_PORT`, default `5173`
- `IKP_API_PUBLIC_HOST`, default `localhost`
- `IKP_UI_PUBLIC_HOST`, optional extra CORS origin host
- `VITE_API_BASE_URL`, overrides the frontend API URL
- `CORS_ALLOWED_ORIGINS`, comma-separated FastAPI allowlist

## Implemented Capabilities

- Repository bootstrap from OKF Markdown into an in-memory graph.
- Source registration with file hash deduplication and persisted `repository/manifest.json`.
- PDF extraction with an adapter boundary, currently including HPE QuickSpecs logic.
- Excel extraction for structured `Components` and `SKUs` sheets, with optional platform linking.
- OKF reader/writer round trip for canonical ontology objects.
- NetworkX graph traversal for compatibility, relationships, category limits, dependencies, and solution-domain isolation.
- Gemini-backed intent parsing and component selection, with graceful fallbacks when the key is missing.
- Gemini embedding based semantic search through ChromaDB.
- BOQ validation with exact/fuzzy matching, invalid SKU reporting, platform inference, rule evaluation, and alternative solution suggestions.
- A LangGraph workflow with bounded draft/validate attempts and placeholder nodes for future dynamic integrations.
- A React/Vite UI for dashboard, BOQ validation, semantic search, solution synthesis, review queue, and KT.
- MCP server entry point for external agent access to status/query operations.

## Partial Or Placeholder Capabilities

- Live partner/vendor portal validation is a placeholder. `live_portal_validation` currently returns success without contacting an external system.
- Human-in-the-loop workflow nodes exist, and the UI has a review queue, but there is not yet a complete approve/reject/resume workflow for every `KnowledgeDelta`.
- Cost estimates in BOQ alternatives are static profile placeholders, not live pricing.
- Semantic search depends on successful Gemini embeddings and a populated ChromaDB index. Without `GEMINI_API_KEY`, vector queries return empty or degraded results.
- Rule extraction through Antigravity CLI helpers is available but depends on the local `antigravity-cli` command being installed and configured.
- `make typecheck` is not currently a release gate; mypy has a known backlog.

## Not In Scope Yet

The following are architectural intentions from earlier standards, not current runtime behavior:

- Real partner portal login, scraping, API calls, stock checks, or price checks.
- A persistent graph database such as Neo4j or Neptune.
- Multi-tenant customer isolation.
- Production deployment, security hardening, or cloud observability pipelines.

## Developer And Agent Rules

- Prefer `./scripts/start_api.sh` and `./scripts/start_ui.sh` over hand-written `uvicorn` or `vite` commands.
- Use `uv run` for Python commands, for example `uv run pytest -q`.
- Use `npm run <script>` inside `ikp_web/` for frontend commands.
- Keep the boundary clear:
  - Knowledge Graph means static engineering facts from OKF.
  - LangGraph means process flow for a customer request.
- Do not claim a capability is implemented just because a blueprint describes it. Check code and tests.
- Update this file whenever implementation choices materially change.

## Verification Commands

```bash
uv run pytest -q
npm run build --prefix ikp_web
make lint
make typecheck
git diff --check
```

Current known status after the latest audit: pytest, frontend build, Ruff lint, and diff whitespace checks pass. `make typecheck` still reports the existing mypy backlog and should be treated as a planned cleanup track until fixed.
