# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 91 files · ~38,272 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 782 nodes · 2029 edges · 69 communities (53 shown, 16 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 384 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a828a143`
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
- __init__.py
- SlotMapping
- BaseEngineeringObject
- ._compute_path
- SourceWatcher
- build_workflow_graph
- shared_temp_dir
- temp_dir
- ._process_structured_components
- .semantic_search
- .execute_query
- PlatformDashboard.tsx
- BaseModel
- Path
- .apply_delta
- ingest_catalog.py
- telemetry_trace
- .semantic_search

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 67 edges
2. `GraphBuilder` - 65 edges
3. `Platform` - 58 edges
4. `BaseEngineeringObject` - 55 edges
5. `RepoManager` - 54 edges
6. `EvidenceRecord` - 53 edges
7. `OKFReader` - 43 edges
8. `RuleEngine` - 42 edges
9. `TestGraphBuilder` - 42 edges
10. `EngineeringRelationship` - 41 edges

## Surprising Connections (you probably didn't know these)
- `TestExcelIngestion` --uses--> `ExcelExtractor`  [INFERRED]
  tests/test_excel_parser.py → ikp_platform/core/ingestion/excel_parser.py
- `TestIngestion` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (69 total, 16 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.09
Nodes (25): Configuration, EngineeringAttribute, A typed, structured engineering attribute., Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, SolutionCategory (+17 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.23
Nodes (9): BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, BaseModel, A single message from a validation check., Complete result of validating a solution candidate.     Blueprint 06 §9: Portal, Validate a solution against vendor systems.          Args:             solution_, ValidationMessage (+1 more)

### Community 2 - "IntentParser"
Cohesion: 0.08
Nodes (13): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+5 more)

### Community 3 - "RepoManager"
Cohesion: 0.06
Nodes (33): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+25 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "Component"
Cohesion: 0.09
Nodes (18): Any, Run a user query through the end-to-end multi-step pipeline., Conditional edge router based on BOM validation., Conditional edge router for portal validation failures., should_human_intervene(), should_loop_bom(), Any, [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals. (+10 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.10
Nodes (12): GraphBuilder, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On)., Return graph statistics for observability. (+4 more)

### Community 7 - "App.tsx"
Cohesion: 0.09
Nodes (20): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+12 more)

### Community 8 - "models.py"
Cohesion: 0.29
Nodes (4): Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 9 - "cli.py"
Cohesion: 0.32
Nodes (6): call_tool(), get_repo(), list_tools(), List available tools., TextContent, Tool

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.22
Nodes (3): Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already, TestFuzzyMatching

### Community 12 - "RuleEngine"
Cohesion: 0.20
Nodes (5): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 15 - "._extract_platform_identity"
Cohesion: 0.25
Nodes (7): api_client(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir(), temp_repo()

### Community 16 - "Platform"
Cohesion: 0.14
Nodes (8): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu

### Community 18 - "SourceRegistry"
Cohesion: 0.15
Nodes (21): Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, DeltaStatus, LifecycleStatus, PackagingType, ProcessingStatus, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Product lifecycle status for engineering objects. (+13 more)

### Community 19 - "Platform"
Cohesion: 0.18
Nodes (8): OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re, TestOKFWriter

### Community 21 - "LearningEngine"
Cohesion: 0.14
Nodes (10): FastAPI, lifespan(), (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor (+2 more)

### Community 22 - "SKU"
Cohesion: 0.17
Nodes (13): Extract memory specifications., CategoryLimit, Component, EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category, TestCategoryLimits (+5 more)

### Community 23 - "BOQValidator"
Cohesion: 0.21
Nodes (8): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Rule severity levels., An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Minimum relationship types from Blueprint 03 §7., RelationshipType, Rule, RuleSeverity, TestIngestion

### Community 24 - "Component"
Cohesion: 0.17
Nodes (8): DataFrame, Parse a dataframe of components., Parse a dataframe of SKUs., Extract processor specifications from QuickSpecs tables., Extract storage / drive cage specifications., Extract power supply specifications., EvidenceRecord, Tracks provenance of an engineering fact.     Blueprint 06 §7: "Never overwrite

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - ".filter_by_metadata"
Cohesion: 0.16
Nodes (11): Constraint, An engineering limitation (max controllers, max drives, max memory, etc.).     B, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, Regression tests for IKP V1.0 Phase 1 — Foundation Layer.  Tests: 1. Ontology mo, Blueprint 04 §5: Source must have permanent identity with full metadata., Blueprint 05 §13: Solution must include reasoning and confidence., Create a temporary directory for test artifacts. (+3 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "__init__.py"
Cohesion: 0.13
Nodes (38): ABC, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status(), BaseModel (+30 more)

### Community 49 - "SlotMapping"
Cohesion: 0.16
Nodes (13): datetime, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, BaseEngineeringObject, HistoryEntry, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., _utcnow() (+5 more)

### Community 50 - "BaseEngineeringObject"
Cohesion: 0.12
Nodes (11): PDFExtractor, Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does (+3 more)

### Community 51 - "._compute_path"
Cohesion: 0.17
Nodes (16): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf, Direct regression test for the specific dedup bug found in the     2026-07-18 au (+8 more)

### Community 52 - "SourceWatcher"
Cohesion: 0.17
Nodes (6): Stage 1: Normalize invisible PDF typography and Unicode artifacts., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract high-level Workloads (Customer Intent) and link to Platform., Extract networking/OCP/NIC information., Extract GPU/accelerator information., Main extraction entry point.         Returns (list of engineering objects, knowl

### Community 53 - "build_workflow_graph"
Cohesion: 0.11
Nodes (31): CustomerRequest, EngineeringObjectType, Canonical hierarchy levels from Blueprint 03 §3., Structured customer engineering request.     Blueprint 05 §4: Customer requests, IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B (+23 more)

### Community 54 - "shared_temp_dir"
Cohesion: 0.33
Nodes (3): Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges., Get all objects compatible with the given object.

### Community 55 - "temp_dir"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

### Community 56 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

### Community 57 - ".semantic_search"
Cohesion: 0.50
Nodes (3): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria.

### Community 58 - ".execute_query"
Cohesion: 0.31
Nodes (6): Extract spatial topology and slot mappings., Platform, Spatial topology mapping for physical components., A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., SlotMapping, TestTopology

### Community 64 - "Path"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 66 - "ingest_catalog.py"
Cohesion: 0.83
Nodes (3): get_file_checksum(), ingest_all(), Path

## Knowledge Gaps
- **87 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+82 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `PDFExtractor`, `._extract_platform_identity`, `SlotMapping`, `SourceRegistry`, `TestGraphBuilder`, `Platform`, `build_workflow_graph`, `shared_temp_dir`, `BOQValidator`, `LearningEngine`, `.semantic_search`, `SKU`, `.filter_by_metadata`, `._compute_path`, `PlatformDashboard.tsx`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `PDFExtractor` connect `BaseEngineeringObject` to `BaseEngineeringObject`, `IntentParser`, `RepoManager`, `ingest_catalog.py`, `__init__.py`, `SlotMapping`, `SourceRegistry`, `._compute_path`, `SourceWatcher`, `temp_dir`, `SKU`, `BOQValidator`, `._process_structured_components`, `Component`, `.execute_query`, `.filter_by_metadata`, `build_workflow_graph`, `ObsidianMCPClient`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `LearningEngine` to `BaseEngineeringObject`, `.apply_delta`, `IntentParser`, `RepoManager`, `ingest_catalog.py`, `GraphBuilder`, `models.py`, `__init__.py`, `cli.py`, `._extract_platform_identity`, `Platform`, `SlotMapping`, `SourceRegistry`, `Platform`, `TestGraphBuilder`, `BOQValidator`, `Component`, `.filter_by_metadata`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Platform` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`Platform` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 13 INFERRED edges - model-reasoned connections that need verification._