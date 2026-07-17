# Graph Report - ikp_platform  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 407 nodes · 839 edges · 23 communities
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `422dd814`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PDFExtractor
- KnowledgeDelta
- ExcelExtractor
- SolutionGenerator
- GraphBuilder
- LLMClient
- RepoManager
- cli.py
- models.py
- OKFReader
- LearningEngine
- OKFWriter
- BaseEngineeringObject
- logger.py
- TableParser

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 55 edges
2. `BaseEngineeringObject` - 34 edges
3. `RepoManager` - 31 edges
4. `EvidenceRecord` - 29 edges
5. `GraphBuilder` - 26 edges
6. `KnowledgeDelta` - 24 edges
7. `OKFReader` - 24 edges
8. `DeltaChange` - 23 edges
9. `RuleEngine` - 21 edges
10. `SolutionGenerator` - 20 edges

## Surprising Connections (you probably didn't know these)
- `QueryRequest` --uses--> `DeltaChange`  [INFERRED]
  api.py → core/ontology/models.py
- `QueryRequest` --uses--> `DeltaChangeType`  [INFERRED]
  api.py → core/ontology/models.py
- `QueryRequest` --uses--> `EvidenceRecord`  [INFERRED]
  api.py → core/ontology/models.py
- `QueryRequest` --uses--> `IntentParser`  [INFERRED]
  api.py → core/reasoning/intent_parser.py
- `QueryRequest` --uses--> `SolutionGenerator`  [INFERRED]
  api.py → core/reasoning/solution_generator.py

## Import Cycles
- 1-file cycle: `mcp_server.py -> mcp_server.py`

## Communities (23 total, 0 thin omitted)

### Community 0 - "PDFExtractor"
Cohesion: 0.07
Nodes (41): PDFExtractor, Any, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract spatial topology and slot mappings., Extract product description from introductory text. (+33 more)

### Community 1 - "KnowledgeDelta"
Cohesion: 0.09
Nodes (40): ABC, BOQValidationRequest, get_repo(), get_status(), BaseModel, query_solution(), QueryRequest, SearchRequest (+32 more)

### Community 2 - "ExcelExtractor"
Cohesion: 0.07
Nodes (23): ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., Parse a dataframe of components., Path, Source Registry — Registers, classifies, and tracks engineering sources.  Govern (+15 more)

### Community 3 - "SolutionGenerator"
Cohesion: 0.09
Nodes (21): CustomerRequest, CustomerRequirement, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua (+13 more)

### Community 4 - "GraphBuilder"
Cohesion: 0.07
Nodes (16): GraphBuilder, Any, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria. (+8 more)

### Community 5 - "LLMClient"
Cohesion: 0.08
Nodes (13): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+5 more)

### Community 6 - "RepoManager"
Cohesion: 0.10
Nodes (14): Repository Manager — Orchestrates bidirectional sync between OKF files and the i, Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, Load all existing OKF files into the in-memory graph.         Returns the number (+6 more)

### Community 7 - "cli.py"
Cohesion: 0.11
Nodes (20): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+12 more)

### Community 8 - "models.py"
Cohesion: 0.16
Nodes (21): DeltaChangeType, DeltaStatus, LifecycleStatus, PackagingType, ProcessingStatus, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Knowledge Delta lifecycle status., Types of changes a Knowledge Delta can contain. (+13 more)

### Community 9 - "OKFReader"
Cohesion: 0.14
Nodes (11): OKFReader, Path, OKF Reader — Parses existing OKF Markdown files back into Pydantic models.  Gove, Split an OKF file into (frontmatter_dict, body_str)., Extract relationships from the Markdown body's Relationships section., Extract evidence from the Citations section (OKF §8)., Extract text content under a specific heading., Extract a bulleted list under a specific heading. (+3 more)

### Community 10 - "LearningEngine"
Cohesion: 0.11
Nodes (11): LearningEngine, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m (+3 more)

### Community 11 - "OKFWriter"
Cohesion: 0.16
Nodes (10): OKFWriter, Any, Path, OKF Writer — Writes engineering knowledge objects to disk in Open Knowledge Form, Generate an index.md for the given directory listing all .md concepts.         O, Writes engineering knowledge to disk in OKF format., Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file. (+2 more)

### Community 12 - "BaseEngineeringObject"
Cohesion: 0.24
Nodes (9): BaseEngineeringObject, Constraint, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, An engineering limitation (max controllers, max drives, max memory, etc.).     B, Rule, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret (+1 more)

### Community 13 - "logger.py"
Cohesion: 0.33
Nodes (6): Logger, get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger()

### Community 14 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `PDFExtractor` to `KnowledgeDelta`, `ExcelExtractor`, `LLMClient`, `cli.py`, `models.py`, `BaseEngineeringObject`, `TableParser`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepoManager` to `KnowledgeDelta`, `ExcelExtractor`, `SolutionGenerator`, `GraphBuilder`, `LLMClient`, `cli.py`, `models.py`, `OKFReader`, `LearningEngine`, `OKFWriter`, `BaseEngineeringObject`?**
  _High betweenness centrality (0.174) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `BaseEngineeringObject` to `PDFExtractor`, `ExcelExtractor`, `GraphBuilder`, `RepoManager`, `models.py`, `OKFReader`, `LearningEngine`, `OKFWriter`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `PDFExtractor` (e.g. with `cmd_ingest()` and `TableParser`) actually correct?**
  _`PDFExtractor` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `RepoManager` (e.g. with `BOQValidationRequest` and `QueryRequest`) actually correct?**
  _`RepoManager` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `EvidenceRecord` (e.g. with `BOQValidationRequest` and `QueryRequest`) actually correct?**
  _`EvidenceRecord` has 25 INFERRED edges - model-reasoned connections that need verification._