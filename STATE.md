# IKP Platform State

**Last Updated**: 2026-07-20 00:35:00 UTC

## Recent Architecture Changes
* 2026-07-20: Decoupled hardcoded vendor heuristics from `IntentParser` and `SourceRegistry`. 
* 2026-07-20: Dynamic `mandatory_categories` metadata introduced to `Platform` ontology to support non-compute domains (routers, switches). Fixed Pydantic serialization bug silently dropping fields.
* 2026-07-20: Hardened LangGraph Orchestrator Recovery Boundaries (`nodes.py`, `executor.py`, `graph.py`). Implemented `visited_bom_hashes` and `cycle_detected` to prevent infinite loops during recovery resolution. Fixed strict schema alignment for `ValidationFailure`. E2E headless tests verified.

## Knowledge Graph Statistics

| Metric | Value |
|--------|-------|
| Total Nodes | 414 |
| Total Edges | 339 |

## Objects by Type

| Type | Count |
|------|-------|
| Category Limit | 7 |
| Component | 144 |
| Platform | 3 |
| Rule | 165 |
| SKU | 90 |
| Workload | 5 |
