# IKP Engineering Context

**Last Updated**: 2026-07-19 00:00:00 UTC

For current implementation truth, read `IKP/standards/11_CURRENT_IMPLEMENTATION_STACK.md`.
This file is a lightweight project snapshot and may lag generated repository
artifacts.

## Coverage

### Solution Domains

- Compute

### Sources Ingested: 1

## Learnings & Architecture Updates (Agent Run)

- **Semantic Deduplication**: We implemented difflib-based semantic matching during graph ingestion to prevent duplicate `Rule` generation if the node already exists semantically but with slightly different text.
- **Concurrency & Global State**: Found that `lru_cache` on `get_repo` leads to race conditions. Migrated to a threading lock and global `_repo_instance` pattern to support asynchronous workloads securely.
- **Validation UI**: Created `ValidationPortal` for manual review of high-confidence LLM outputs, which allows the human-in-the-loop validation of generated objects.
- **Search Grouping**: The semantic search UI now categorizes results by type (Rule, Category Limit, SKU, Platform) to make the output easier to read.
- **Linear Semantic Score Normalization**: Replaced min-max scaling with linear normalization and dynamic thresholds based on component weights for more stable cross-domain search rankings (ADR-003).
- **Restart Persistence Integrity**: Fixed regex handling in BOQ validation where dotall flags weren't properly serializing/deserializing, ensuring full restart capability of the `RuleEngine` state.
- **Empty Description Handling**: Ensure component extraction from tabular PDFs guards against blank descriptions to prevent trailing hyphens (e.g., "R7N87A - ") in UI labels.
- **LangGraph Orchestrator Integration**: Formalized the separation between the static Knowledge Graph (the "What") and the dynamic LangGraph state machine (the "How"). The workflow now uses bounded draft/validate attempts and routes unresolved human-intervention cases to a terminal placeholder instead of looping forever.
- **[PLANNED/PLACEHOLDER] Live Partner Portal Dynamic Validation Architecture**: Established pipeline placeholders for post-validation live API checks, including temporary vs. permanent error classification, dynamic Knowledge Graph updating (learning from portal rejections), and Human-In-The-Loop (HITL) fallback nodes. This is currently a stub and not an active integration.
- **Observability & Telemetry Standards**: Enforced strict `logging` instantiation across all LangGraph process nodes (`ikp.workflow.nodes`) to ensure complete telemetry. Every state transition and node execution must be observable to track the agent's reasoning loops and portal rejections.
- **Run Script Port Normalization**: `scripts/start_api.sh` and `scripts/start_ui.sh` default to API `8000` and UI `5173`, accept explicit local ports, and normalize accidental leading-`1` five-digit ports such as `18000` and `15173`.
