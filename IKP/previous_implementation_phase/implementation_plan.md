# IKP Version 1.0 — Complete Implementation Plan

This document is the authoritative execution plan for building IKP. It addresses all 14 gaps identified in the architecture audit and maps every component to its governing blueprint.

---

## Contract Hierarchy

When there is ambiguity:

1. **IKP Standards (Blueprints 01–09)** govern business behavior and engineering semantics.
2. **OKF Specification** governs generated document structure and formatting.
3. IKP Standards win on any conflict.

---

## Architectural Foundations

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.10+ | Best ecosystem for PDF extraction, graph processing, LLM integration |
| Persistence | OKF Markdown + YAML frontmatter | Documentation Contract — human-readable, diffable, git-friendly |
| Active Graph | NetworkX DiGraph (in-memory) | Fast metadata filtering, relationship traversal, rule evaluation |
| Reasoning | Deterministic Python rule engine | Guarantees explainability (Blueprint 07 §11) |
| Knowledge Extraction | LLM-driven structured outputs | Converts unstructured sources → Canonical Ontology JSON |
| Sync | Bidirectional OKF ↔ Graph | OKF Reader bootstraps graph on startup; OKF Writer persists changes |

---

## Repository Layout (Human + Antigravity Managed)

```text
vendorsolution_okf/
│
│── IKP/                              # HUMAN MANAGED — never modified by system
│   ├── readme.md                     # Execution order and conventions
│   ├── standards/                    # 9 Blueprints + Checklist
│   │   ├── 01_VISION_AND_BUSINESS_PROBLEM.md
│   │   ├── ...
│   │   └── 10_IMPLEMENTATION_CHECKLIST.md
│   └── references/
│       └── OKF_SPECIFICATION.md      # Documentation Contract
│
│── sources/                          # HUMAN MANAGED — drop files here
│   ├── pdfs/
│   ├── excel/
│   ├── boqs/
│   ├── portals/
│   └── human_feedback/
│
│── repository/                       # ANTIGRAVITY MANAGED — canonical knowledge
│   ├── index.md                      # Root progressive disclosure (OKF §6)
│   ├── log.md                        # Root change history (OKF §7)
│   └── {solution-domain}/            # e.g. storage/, compute/, networking/
│       ├── index.md
│       └── {product-family}/
│           ├── index.md
│           └── {generation}/
│               └── {platform}/
│                   ├── identity.md
│                   ├── summary.md
│                   ├── attributes.md
│                   ├── capabilities.md
│                   ├── components/
│                   │   └── {component}.md
│                   ├── variants/
│                   ├── rules/
│                   ├── relationships/
│                   ├── workloads/
│                   ├── evidence/
│                   └── history/
│
│── history/                          # ANTIGRAVITY MANAGED — knowledge deltas
│   └── {YYYY-MM-DD}_{delta_id}.md
│
│── work/                             # ANTIGRAVITY MANAGED — in-progress processing
│
│── tests/                            # ANTIGRAVITY MANAGED — regression tests
│
│── tools/                            # ANTIGRAVITY MANAGED — utility scripts
│
│── CONTEXT.md                        # ANTIGRAVITY MANAGED — current engineering state
│── STATE.md                          # ANTIGRAVITY MANAGED — platform operational state
│── LOG.md                            # ANTIGRAVITY MANAGED — chronological operations log
│
│── ikp_platform/                     # ANTIGRAVITY MANAGED — Python implementation
│   ├── core/
│   │   ├── ontology/
│   │   │   └── models.py             # All Pydantic models (ontology + lifecycle)
│   │   ├── ingestion/
│   │   │   ├── source_watcher.py     # Detects new files in sources/
│   │   │   ├── source_registry.py    # Registers & classifies sources
│   │   │   └── llm_extractor.py      # LLM-driven knowledge extraction
│   │   ├── repository/
│   │   │   ├── okf_writer.py         # Pydantic → OKF Markdown (with index/log)
│   │   │   ├── okf_reader.py         # OKF Markdown → Pydantic (bootstrap)
│   │   │   ├── graph_builder.py      # Pydantic → NetworkX (with metadata filtering)
│   │   │   └── repo_manager.py       # Orchestrates sync between layers
│   │   ├── reasoning/
│   │   │   ├── intent_parser.py      # Customer request → structured requirements
│   │   │   ├── rule_engine.py        # Deterministic constraint/compatibility evaluation
│   │   │   └── solution_generator.py # Multi-profile candidate generation
│   │   ├── validation/
│   │   │   └── validator.py          # Abstract vendor validation interface
│   │   ├── learning/
│   │   │   └── learning_engine.py    # Knowledge delta merge + repository evolution
│   │   └── observability/
│   │       └── logger.py             # Structured logging + STATE.md updates
│   └── cli.py                        # Command-line interface
│
└── requirements.txt
```

---

## Module Design — Mapped to Blueprints

### 1. Ontology Models (`core/ontology/models.py`)

**Governs:** Blueprint 03 (Engineering Ontology), Blueprint 04 §5 (Source Registration), Blueprint 02 §7 (Knowledge Delta)

All data structures in one file. Every model uses Pydantic for validation and serialization.

| Model | Purpose | Blueprint |
|-------|---------|-----------|
| `BaseEngineeringObject` | Base for all engineering concepts | BP03 §4 |
| `Platform` | Commercially available product platform | BP03 §4 |
| `Component` | CPU, Controller, Drive, DIMM, GPU, etc. | BP03 §4 |
| `SKU` | Commercially orderable item | BP03 §4 |
| `Workload` | Customer intent (AI, VMware, SAP, etc.) | BP03 §11 |
| `Rule` | Engineering rule with scope, confidence, evidence, version | BP03 §8 |
| `Constraint` | Engineering limitation (max controllers, drives, etc.) | BP03 §9 |
| `EngineeringRelationship` | Directed, typed, evidence-backed relationship | BP03 §7 |
| `EvidenceRecord` | Provenance: source, date, confidence, snippet | BP06 §7 |
| `HistoryEntry` | Immutable change record | BP06 §7 |
| `Source` | Registered engineering source with full metadata | BP04 §5 |
| `KnowledgeDelta` | Set of changes from a single ingestion or validation event | BP02 §7 |
| `CustomerRequest` | Structured customer requirement | BP05 §4 |
| `SolutionCandidate` | Generated solution with reasoning and confidence | BP05 §13 |

---

### 2. Source Watcher & Registry (`core/ingestion/`)

**Governs:** Blueprint 04 §4 (Universal Acquisition Pipeline), Blueprint 07 §3

| Component | Responsibility |
|-----------|---------------|
| `source_watcher.py` | Monitors `sources/` for new or changed files |
| `source_registry.py` | Assigns permanent Source ID, classifies type, extracts metadata, preserves original |
| `llm_extractor.py` | Sends raw content to LLM → receives structured JSON → validates → produces `KnowledgeDelta` |

**Pipeline per source:**
```
Detect → Register → Classify → Extract Metadata → LLM Extract → Normalize → 
Ontology Map → Relationship Discovery → Rule Discovery → Knowledge Candidate → 
Validate → Knowledge Delta → Canonical Repository → Indexes → Ready for Reasoning
```

---

### 3. Repository Layer (`core/repository/`)

**Governs:** Blueprint 06 (Canonical Repository), OKF Spec §3–§7

| Component | Responsibility |
|-----------|---------------|
| `okf_writer.py` | Writes `BaseEngineeringObject` → OKF Markdown with full frontmatter (type, title, vendor, generation, product_family, solution_domain, capabilities, lifecycle_status, tags, timestamp). Generates `index.md` per directory. Appends to `log.md`. |
| `okf_reader.py` | Parses existing OKF Markdown → reconstructs Pydantic models. Enables bootstrap from cold start. |
| `graph_builder.py` | Loads Pydantic objects into NetworkX DiGraph. Provides `filter_by_metadata(criteria)` for search-space reduction. Provides `traverse_relationships(node_id, rel_type)`. |
| `repo_manager.py` | Orchestrates bidirectional sync. On startup: OKF Reader → Graph Builder. On change: Graph Builder + OKF Writer. Updates `CONTEXT.md`, `STATE.md`, `LOG.md`. |

**Hierarchical path derivation:**
```python
# Object with: solution_domain="storage", product_family="alletra", 
#              generation="6000", platform="alletra-6050"
# Produces path: repository/storage/alletra/6000/alletra-6050/identity.md
```

---

### 4. Reasoning Engine (`core/reasoning/`)

**Governs:** Blueprint 05 (Engineering Reasoning & Solution Synthesis), Blueprint 07 §6–§7

| Component | Responsibility |
|-----------|---------------|
| `intent_parser.py` | Converts natural language / BOQ → `CustomerRequest` with structured requirements (business, technical, operational, commercial) |
| `rule_engine.py` | Walks the graph evaluating: capabilities → rules → dependencies → constraints → relationships → compatibility → workloads → evidence → confidence. Every evaluation step is recorded for explainability. |
| `solution_generator.py` | Generates multiple `SolutionCandidate` objects optimized for different profiles (Lowest Cost, Balanced, Performance, AI Optimized, etc.). Each includes full reasoning chain, evidence, trade-offs, and confidence score. |

---

### 5. Validation Loop (`core/validation/`)

**Governs:** Blueprint 02 §8, Blueprint 05 §12, Blueprint 06 §8–§9, Blueprint 07 §8

| Component | Responsibility |
|-----------|---------------|
| `validator.py` | Abstract `VendorValidator` base class. `ValidationResult` model with errors, warnings, recommendations, dependency failures. V1.0 stub: manual human review mode. Future: portal API integration. |

Every `ValidationResult` produces a `KnowledgeDelta` that feeds back into the Learning Loop.

---

### 6. Learning Loop (`core/learning/`)

**Governs:** Blueprint 02 §9, Blueprint 06 §12, Blueprint 07 §12

| Component | Responsibility |
|-----------|---------------|
| `learning_engine.py` | Accepts `KnowledgeDelta` from any source (ingestion, validation, human feedback). Validates delta. Merges approved changes into canonical graph + OKF repository. Appends to `history/`. Updates `LOG.md`. |

**Learning sources:** Updated PDFs, new products, firmware updates, portal validation, configuration errors, portal advice, human review, customer deployments, engineering corrections.

---

### 7. Observability (`core/observability/`)

**Governs:** Blueprint 02 §11

| Component | Responsibility |
|-----------|---------------|
| `logger.py` | Structured Python logging for all pipeline stages. Periodically updates `STATE.md` with: graph node count, edge count, rule count, source count, last ingestion, pending reviews, repository health. |

---

### 8. Human Collaboration (`cli.py`)

**Governs:** Blueprint 02 §10, Blueprint 07 §13

The CLI will:
- Ingest sources: `ikp ingest <path>`
- Query knowledge: `ikp query "AI-ready storage with replication"`
- Review pending deltas: `ikp review`
- Approve/reject human review items: `ikp approve <delta_id>`
- Show platform state: `ikp status`

Human review is triggered automatically when: conflicting evidence exists, confidence is insufficient, ontology mapping fails, new concepts are discovered, vendor information conflicts.

---

## Execution Phases

### Phase 1 — Foundation (Ontology + Repository Mechanics)

- [x] Project scaffolding
- [ ] **Rewrite `models.py`** — add all 14 models with full fields per audit
- [ ] **Create `okf_writer.py`** — hierarchical paths, full frontmatter, index.md, log.md
- [ ] **Create `okf_reader.py`** — parse existing OKF files → Pydantic models
- [ ] **Enhance `graph_builder.py`** — metadata filtering, relationship traversal by type
- [ ] **Create `repo_manager.py`** — bidirectional sync orchestration
- [ ] **Populate `CONTEXT.md`, `STATE.md`, `LOG.md`** with initial content

### Phase 2 — Knowledge Acquisition Pipeline

- [ ] **Create `source_watcher.py`** — filesystem monitoring
- [ ] **Create `source_registry.py`** — source classification and registration
- [ ] **Create `llm_extractor.py`** — LLM-driven extraction with structured outputs
- [ ] **Ingest first PDF** — end-to-end validation

### Phase 3 — Engineering Reasoning

- [ ] **Create `intent_parser.py`** — customer request normalization
- [ ] **Create `rule_engine.py`** — deterministic constraint evaluation
- [ ] **Create `solution_generator.py`** — multi-profile candidate generation

### Phase 4 — Validation & Learning

- [ ] **Create `validator.py`** — abstract interface + manual review stub
- [ ] **Create `learning_engine.py`** — delta merge + repository evolution

### Phase 5 — Integration & Polish

- [ ] **Create `logger.py`** — observability
- [ ] **Create `cli.py`** — command-line interface
- [ ] **Write regression tests** — per checklist
- [ ] **End-to-end test** — ingest source → query → generate solution → validate → learn

---

## Verification Plan

### Automated Tests
```bash
pytest tests/ -v
```
- `test_ontology.py` — validate all model constraints and serialization
- `test_okf_writer.py` — verify OKF conformance (frontmatter, structure, index/log)
- `test_okf_reader.py` — round-trip: write → read → compare
- `test_graph_builder.py` — metadata filtering, path traversal, dependency resolution
- `test_rule_engine.py` — constraint enforcement with synthetic engineering data
- `test_solution_generator.py` — multi-profile generation correctness
- `test_learning_engine.py` — delta merge preserves history and evidence

### Manual Verification
- Ingest the provided PDF end-to-end
- Open `repository/` in Obsidian and verify graph visualization
- Run a customer query and inspect the explainable solution output
- Verify `LOG.md`, `STATE.md`, `CONTEXT.md` are automatically maintained

### Implementation Checklist Mapping

| Checklist Item | Module | Phase |
|---------------|--------|-------|
| □ Repository created | `repo_manager.py` | 1 |
| □ Source watcher implemented | `source_watcher.py` | 2 |
| □ PDF parser implemented | `llm_extractor.py` | 2 |
| □ Excel parser implemented | `llm_extractor.py` | 2 |
| □ Portal parser implemented | `llm_extractor.py` (stub) | 2 |
| □ Metadata extraction implemented | `source_registry.py` | 2 |
| □ Ontology implemented | `models.py` | 1 |
| □ Knowledge graph implemented | `graph_builder.py` | 1 |
| □ Rule engine implemented | `rule_engine.py` | 3 |
| □ Recommendation engine implemented | `solution_generator.py` | 3 |
| □ Validation loop implemented | `validator.py` | 4 |
| □ Learning loop implemented | `learning_engine.py` | 4 |
| □ Repository generation implemented | `okf_writer.py` | 1 |
| □ Regression tests passing | `tests/` | 5 |
