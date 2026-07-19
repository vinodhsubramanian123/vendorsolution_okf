# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 80 files · ~35,217 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 693 nodes · 1794 edges · 62 communities (49 shown, 13 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 370 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4f840d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- BaseEngineeringObject
- EvidenceRecord
- IntentParser
- RepoManager
- devDependencies
- Component
- GraphBuilder
- App.tsx
- models.py
- cli.py
- compilerOptions
- PDFExtractor
- RuleEngine
- compilerOptions
- Setup
- ._extract_platform_identity
- Platform
- TestGraphBuilder
- SourceRegistry
- Platform
- ObsidianMCPClient
- LearningEngine
- SKU
- BOQValidator
- Component
- Coverage
- test_mcp_integration.py
- .filter_by_metadata
- IKP Platform State
- test_api_endpoints.py
- tsconfig.json
- IKP Operations Log
- bootstrap.sh
- start_api.sh
- start_ui.sh
- agy
- pip
- python
- list_models.py
- SlotMapping
- BaseModel
- .reindex_vector_store
- .update_context
- api_client
- shared_temp_dir
- temp_dir
- BaseEngineeringObject
- GraphBuilder
- .apply_delta
- ingest_catalog.py
- ._extract_list_section
- ._extract_section

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 67 edges
2. `BaseEngineeringObject` - 55 edges
3. `Platform` - 53 edges
4. `RepoManager` - 53 edges
5. `GraphBuilder` - 52 edges
6. `EvidenceRecord` - 51 edges
7. `OKFReader` - 43 edges
8. `TestGraphBuilder` - 41 edges
9. `KnowledgeDelta` - 38 edges
10. `EngineeringRelationship` - 37 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (62 total, 13 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.11
Nodes (27): datetime, Enum, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, ConfidenceLevel, Configuration, DeltaStatus, HistoryEntry, PackagingType (+19 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.06
Nodes (62): ABC, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status(), BaseModel (+54 more)

### Community 2 - "IntentParser"
Cohesion: 0.09
Nodes (15): Intent Parser — Extracts structured engineering requirements from natural langua, LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep (+7 more)

### Community 3 - "RepoManager"
Cohesion: 0.12
Nodes (20): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+12 more)

### Community 4 - "devDependencies"
Cohesion: 0.06
Nodes (33): axios, dependencies, axios, lucide-react, react, react-dom, devDependencies, oxlint (+25 more)

### Community 5 - "Component"
Cohesion: 0.21
Nodes (7): Path, Attempt to infer vendor from filename., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., Compute SHA-256 hash of a file for duplicate detection., SourceRegistry

### Community 6 - "GraphBuilder"
Cohesion: 0.10
Nodes (11): Any, GraphBuilder, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On). (+3 more)

### Community 7 - "App.tsx"
Cohesion: 0.10
Nodes (19): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), PlatformDashboard(), SemanticSearch() (+11 more)

### Community 8 - "models.py"
Cohesion: 0.24
Nodes (6): OKFReader, Path, Split an OKF file into (frontmatter_dict, body_str)., Parses OKF Markdown files and reconstructs Pydantic engineering objects., Recursively scan the repository and parse all concept files.         Skips reser, Parse an OKF Markdown file that may contain multiple Pydantic models.

### Community 9 - "cli.py"
Cohesion: 0.33
Nodes (5): call_tool(), list_tools(), List available tools., TextContent, Tool

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 12 - "RuleEngine"
Cohesion: 0.13
Nodes (14): EngineeringObjectType, Canonical hierarchy levels from Blueprint 03 §3., Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluates a set of component IDs against the canonical graph to ensure     all c, Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er (+6 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 15 - "._extract_platform_identity"
Cohesion: 0.11
Nodes (12): PDFExtractor, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags. (+4 more)

### Community 16 - "Platform"
Cohesion: 0.29
Nodes (4): Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 17 - "TestGraphBuilder"
Cohesion: 0.23
Nodes (4): Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, Create a small test graph with known structure., TestGraphBuilder

### Community 18 - "SourceRegistry"
Cohesion: 0.16
Nodes (13): Constraint, LifecycleStatus, Product lifecycle status for engineering objects., An engineering limitation (max controllers, max drives, max memory, etc.).     B, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, OKF Writer — Writes engineering knowledge objects to disk in Open Knowledge Form, Regression tests for IKP V1.0 Phase 1 — Foundation Layer.  Tests: 1. Ontology mo (+5 more)

### Community 19 - "Platform"
Cohesion: 0.29
Nodes (7): Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., OKFWriter, Writes engineering knowledge to disk in OKF format., Write an object, read it back, verify key fields match., TestOKFReader, TestOKFWriter

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.18
Nodes (8): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source, main(), main(), main(), Blueprint 04 §5: Source must have permanent identity with full metadata., TestIngestion

### Community 21 - "LearningEngine"
Cohesion: 0.14
Nodes (8): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu

### Community 22 - "SKU"
Cohesion: 0.19
Nodes (8): BaseEngineeringObject, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Add a concept and all its attributes as a node in the graph., Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re

### Community 23 - "BOQValidator"
Cohesion: 0.12
Nodes (9): DataFrame, Parse a dataframe of components., Parse a dataframe of SKUs., Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU (+1 more)

### Community 24 - "Component"
Cohesion: 0.16
Nodes (13): CategoryLimit, Component, A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category, Minimum relationship types from Blueprint 03 §7., RelationshipType, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, api_client() (+5 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - ".filter_by_metadata"
Cohesion: 0.25
Nodes (5): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all objects compatible with the given object.

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 47 - "list_models.py"
Cohesion: 0.23
Nodes (9): ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parses Excel spreadsheets into IKP canonical objects., Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ProcessingStatus, Source classification from Blueprint 04 §3., Source processing lifecycle status., SourceType (+1 more)

### Community 49 - "SlotMapping"
Cohesion: 0.60
Nodes (3): Spatial topology mapping for physical components., SlotMapping, TestTopology

### Community 50 - "BaseModel"
Cohesion: 0.20
Nodes (7): Extract high-level Workloads (Customer Intent) and link to Platform., Extract memory specifications., EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., Extract relationships from the Markdown body's Relationships section., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, temp_repo()

### Community 51 - ".reindex_vector_store"
Cohesion: 0.22
Nodes (6): (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor

### Community 52 - ".update_context"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis

### Community 53 - "api_client"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 55 - "temp_dir"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

### Community 56 - "BaseEngineeringObject"
Cohesion: 0.33
Nodes (5): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, Blueprint 03 §8: Rule must expose scope, confidence, evidence, version., Test that relationships (edges) and body contents survive a restart/roundtrip., test_okf_persistence_roundtrip()

### Community 57 - "GraphBuilder"
Cohesion: 0.50
Nodes (3): Extract power supply specifications., EngineeringAttribute, A typed, structured engineering attribute.

### Community 59 - "ingest_catalog.py"
Cohesion: 0.83
Nodes (3): get_file_checksum(), ingest_all(), Path

## Knowledge Gaps
- **84 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `._extract_platform_identity` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `RepoManager`, `RuleEngine`, `TestGraphBuilder`, `SourceRegistry`, `Platform`, `ObsidianMCPClient`, `SKU`, `BOQValidator`, `Component`, `SlotMapping`, `BaseModel`, `.update_context`, `shared_temp_dir`, `temp_dir`, `BaseEngineeringObject`, `GraphBuilder`, `ingest_catalog.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `GraphBuilder` to `BaseEngineeringObject`, `EvidenceRecord`, `models.py`, `RuleEngine`, `TestGraphBuilder`, `SourceRegistry`, `.reindex_vector_store`, `ObsidianMCPClient`, `Platform`, `SKU`, `BOQValidator`, `Component`, `.filter_by_metadata`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `.reindex_vector_store` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `RepoManager`, `GraphBuilder`, `models.py`, `cli.py`, `Platform`, `TestGraphBuilder`, `SourceRegistry`, `Platform`, `LearningEngine`, `SKU`, `Component`, `BaseModel`, `.update_context`, `BaseEngineeringObject`, `.apply_delta`, `ingest_catalog.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Platform` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`Platform` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 20 INFERRED edges - model-reasoned connections that need verification._