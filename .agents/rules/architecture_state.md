---
description: "Current state of the core architecture implementation (Models, Persistence, Ingestion)"
---

# Architecture Implementation State

This document serves as Knowledge Transfer (KT) for agents regarding the core architectural components of the VendorSolution OKF platform. It clarifies areas that were historically incomplete but are now fully implemented, avoiding the need for redundant abstractions.

## 1. Persistence & Delta Store
- **File System as Source of Truth**: The `repository/` directory is the canonical state. It uses a **hierarchical layout** (e.g., `repository/compute/`, `repository/storage/`). **No flat-to-hierarchy migration is needed.**
- **Delta Persistence**: There is no dedicated `DeltaStore` database or abstraction. `KnowledgeDelta` records are safely persisted as Markdown logs in the `history/` directory via `RepoManager._record_delta` and are held in memory by `LearningEngine.pending_deltas`. Do not attempt to build a separate `DeltaStore` module.

## 2. Ingestion & Orchestration
- **Ingestion Script**: The ingestion loop is fully orchestrated by `ikp_platform/scripts/ingest_catalog.py`. It reads PDFs, checks a `manifest.json` for checksums, extracts `KnowledgeDelta` objects, and uses the `RepoManager` to apply them.
- **Source Registry**: `source_watcher.py` and `source_registry.py` handle basic watching and registration. 

## 3. OKF Sync (Bidirectional)
- **OKF Writer**: The `OKFWriter` generates the hierarchical folder structure, serializes objects to frontmatter, and handles index/log generation (`index.md`, `log.md`).
- **OKF Reader**: The `OKFReader` provides full bidirectional synchronization, capable of parsing the hierarchical markdown back into Pydantic models.

## 4. Graph Construction & Context Passing
- **Graph Builder**: `GraphBuilder` (`ikp_platform/core/repository/graph_builder.py`) maintains the in-memory NetworkX graph.
- **Context Filtering**: It supports rich metadata filtering (`filter_by_metadata`) and can extract induced subgraphs (`build_subgraph`) to pass narrowed context to the LLM reasoning engine.

## 5. Observability
- **State Management**: `RepoManager` automatically maintains `STATE.md` and `CONTEXT.md` in the root repository folder, as well as root-level `LOG.md`. 
- DO NOT manually update these files; allow `RepoManager` and `OKFWriter` to manage them.

## 6. Ontology Models
- **Core Models**: All core models (`Source`, `KnowledgeDelta`, `EvidenceRecord`, `HistoryEntry`, `Rule`) are fully implemented and enriched in `ikp_platform/core/ontology/models.py`. Use these existing Pydantic models instead of reinventing them.
