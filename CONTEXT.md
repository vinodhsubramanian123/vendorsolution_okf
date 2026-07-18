# IKP Engineering Context

**Last Updated**: 2026-07-17 20:13:08 UTC

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
