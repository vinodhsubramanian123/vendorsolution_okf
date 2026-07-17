# Graph Report - vendorsolution_okf  (2026-07-18)

## Corpus Check
- 72 files · ~43,954 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 346 nodes · 856 edges · 18 communities (15 shown, 3 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `41c52bc1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- IKP Platform State
- Vendorsolution OKF
- Cross-Platform Toolchain Setup
- agy
- pip
- python
- api.py
- PDFExtractor
- RepoManager
- LLMClient
- App.tsx
- BaseModel
- ._read_frontmatter
- Source
- TableParser
- Coverage
- IKP Operations Log
- conftest.py

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 60 edges
2. `OKFReader` - 34 edges
3. `EvidenceRecord` - 33 edges
4. `BaseEngineeringObject` - 33 edges
5. `RepoManager` - 30 edges
6. `DeltaChange` - 24 edges
7. `RuleEngine` - 24 edges
8. `Platform` - 23 edges
9. `KnowledgeDelta` - 22 edges
10. `ConfidenceLevel` - 21 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `PDFExtractor`  [EXTRACTED]
  tests/integration/test_gen12_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `main()` --calls--> `PDFExtractor`  [EXTRACTED]
  tests/integration/test_real_boq.py → ikp_platform/core/ingestion/pdf_extractor.py
- `main()` --calls--> `PDFExtractor`  [EXTRACTED]
  tests/integration/test_storage_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `main()` --calls--> `RuleEngine`  [EXTRACTED]
  tests/integration/test_domain_isolation.py → ikp_platform/core/reasoning/rule_engine.py
- `main()` --calls--> `RuleEngine`  [EXTRACTED]
  tests/integration/test_real_boq.py → ikp_platform/core/reasoning/rule_engine.py

## Import Cycles
- None detected.

## Communities (18 total, 3 thin omitted)

### Community 0 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 1 - "Vendorsolution OKF"
Cohesion: 0.33
Nodes (5): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF

### Community 2 - "Cross-Platform Toolchain Setup"
Cohesion: 0.06
Nodes (63): datetime, Enum, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, BaseEngineeringObject, CategoryLimit, Component, Configuration, Constraint (+55 more)

### Community 6 - "api.py"
Cohesion: 0.09
Nodes (47): ABC, BOQValidationRequest, get_repo(), get_status(), BaseModel, query_solution(), QueryRequest, SearchRequest (+39 more)

### Community 7 - "PDFExtractor"
Cohesion: 0.07
Nodes (33): PDFExtractor, Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract spatial topology and slot mappings. (+25 more)

### Community 8 - "RepoManager"
Cohesion: 0.07
Nodes (29): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+21 more)

### Community 9 - "LLMClient"
Cohesion: 0.12
Nodes (11): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+3 more)

### Community 10 - "App.tsx"
Cohesion: 0.20
Nodes (7): BoqValidation(), PlatformDashboard(), SemanticSearch(), Sidebar(), SidebarProps, ChatMessage, SolutionSynthesis()

### Community 11 - "BaseModel"
Cohesion: 0.19
Nodes (11): CustomerRequest, CustomerRequirement, HistoryEntry, BaseModel, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom (+3 more)

### Community 12 - "._read_frontmatter"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 13 - "Source"
Cohesion: 0.36
Nodes (5): Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source, main(), main(), main()

### Community 14 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

### Community 15 - "Coverage"
Cohesion: 0.40
Nodes (4): Coverage, IKP Engineering Context, Solution Domains, Sources Ingested: 1

### Community 16 - "IKP Operations Log"
Cohesion: 0.40
Nodes (4): 2026-07-15, 2026-07-16, 2026-07-17, IKP Operations Log

### Community 17 - "conftest.py"
Cohesion: 0.40
Nodes (4): empty_graph(), Returns a clean GraphBuilder instance., Create a shared temporary directory for test artifacts., shared_temp_dir()

## Knowledge Gaps
- **12 isolated node(s):** `Solution Domains`, `Sources Ingested: 1`, `2026-07-17`, `2026-07-16`, `2026-07-15` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `PDFExtractor` to `Cross-Platform Toolchain Setup`, `api.py`, `RepoManager`, `LLMClient`, `Source`, `TableParser`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepoManager` to `Cross-Platform Toolchain Setup`, `api.py`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `Cross-Platform Toolchain Setup` to `RepoManager`, `BaseModel`, `PDFExtractor`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `OKFReader` (e.g. with `BaseEngineeringObject` and `CategoryLimit`) actually correct?**
  _`OKFReader` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `EvidenceRecord` (e.g. with `BOQValidationRequest` and `QueryRequest`) actually correct?**
  _`EvidenceRecord` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `BaseEngineeringObject` (e.g. with `PDFExtractor` and `OKFReader`) actually correct?**
  _`BaseEngineeringObject` has 4 INFERRED edges - model-reasoned connections that need verification._