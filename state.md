# IKP Platform - Current System State

## Architecture Status (v2.0)
- **AI Extraction Pipeline:** Successfully migrated from cloud-based rate-limited `google-genai` to local `antigravity-cli` (v2.0) using parallel subprocess architecture. Token authentication is persisted via OAuth2/PKCE.
- **Fault Tolerance:** Pipeline falls back to deterministic regex extraction if the local AI CLI times out or errors.
- **Evidence Cross-Referencing:** Obsidian MCP Search is actively integrated during extraction to ground AI-generated rules with local engineering documentation.
- **Rule Engine:** Upgraded to surface the actual `description` and `expected_outcome` of rules rather than generic fallback titles (e.g. "Engineering Rule 88"), providing transparent traceability.

## Application Status
- **FastAPI Backend (Port 8000):** Online. Supports `/api/status` (with Platform KPIs), `/api/query` (Solution Synthesis), `/api/boq/validate` (BOQ Engine), and `/api/search` (Vector Store Semantic Search).
- **React Frontend (Port 5173):** Online.
  - **Graph Dashboard:** Renders specific product KPIs (SKUs, Categories, Rules by Platform).
  - **BOQ Validation:** Supports both text-area pasting and CSV file upload for fuzzy-matching and validating SKUs against the rules engine.
  - **Semantic Search:** Provides vector-based semantic search over the engineering knowledge graph.

## Known Gaps / Pending Items
- None at this time. All gaps identified during the v2.0 audit have been successfully resolved and tested end-to-end.
