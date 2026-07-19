# Graph Report - vendorsolution_okf  (2026-07-20)

## Corpus Check
- 105 files · ~46,189 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 923 nodes · 2242 edges · 87 communities (64 shown, 23 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 387 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94395d0e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- OKFReader
- TableParser
- LLMClient
- cli.py
- devDependencies
- WorkflowNodes
- GraphBuilder
- App.tsx
- EvidenceRecord
- IntentParser
- compilerOptions
- SolutionGenerator
- ConfidenceLevel
- compilerOptions
- Setup
- Component
- BaseEngineeringObject
- TestGraphBuilder
- TestOKFWriter
- graph.py
- RuleEngine
- RepoManager
- Platform
- api.py
- ExcelExtractor
- Coverage
- test_mcp_integration.py
- test_foundation.py
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
- api.py
- SourceRegistry
- Source
- test_graph_field_parity.py
- Platform
- CustomerRequest
- RepositoryWatcher
- ExcelExtractor
- conftest.py
- .extract
- logger.py
- ._read_frontmatter
- mcp_server.py
- SourceWatcher
- IKPPlatformUser
- scripts
- .build_subgraph
- TestPlatformIdentityAgainstRealPDFs
- .traverse_relationships
- package.json
- TestFuzzyMatching
- .can_handle
- telemetry_trace
- list_tools
- ._normalize_text
- @testing-library/dom
- @testing-library/jest-dom
- typescript
- vite
- @vitejs/plugin-react
- vitest
- SolutionCandidate

## God Nodes (most connected - your core abstractions)
1. `Platform` - 71 edges
2. `BaseEngineeringObject` - 62 edges
3. `HPEQuickSpecsAdapter` - 61 edges
4. `RepoManager` - 55 edges
5. `EvidenceRecord` - 51 edges
6. `GraphBuilder` - 49 edges
7. `Component` - 47 edges
8. `EngineeringRelationship` - 45 edges
9. `RuleEngine` - 43 edges
10. `Source` - 42 edges

## Surprising Connections (you probably didn't know these)
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestCategoryLimits` --uses--> `RelationshipType`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (87 total, 23 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.10
Nodes (20): Configuration, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, SolutionCategory, Variant, OKFReader, Any (+12 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.20
Nodes (14): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_scan(), cmd_status(), cmd_validate(), main(), IKP CLI — Command-line interface for the Infrastructure Knowledge Platform.  Usa (+6 more)

### Community 3 - "cli.py"
Cohesion: 0.28
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 4 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, jsdom, oxlint, @playwright/test, @testing-library/react, @types/node, @types/react, @types/react-dom (+7 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.16
Nodes (10): Any, Deterministically validate the drafted BOM using the static RuleEngine., Dynamically recover from validation failures.         1. Try next candidate in r, [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., Aggregate validation errors and portal rejections into a full-solution FailureRe, Traverse HasSKU edges and rank solutions based on business logic and track delta, Parse the unstructured customer message into strict requirements. (+2 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.15
Nodes (17): CompiledStateGraph, Any, Workflow Executor — API/CLI entry point for running the LangGraph state machine., Run a user query through the end-to-end multi-step pipeline., build_workflow_graph(), Workflow Graph — Defines the LangGraph state machine structure and conditional e, Conditional edge router based on BOM validation with bounded retries., Conditional edge router after select_recovery_strategy. (+9 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (28): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+20 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 9 - "IntentParser"
Cohesion: 0.05
Nodes (27): Client, ComponentSelectionResult, IntentParseResult, KeyManager, LLMClient, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and (+19 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.23
Nodes (7): Path, Compute SHA-256 hash of a file for duplicate detection., Attempt to infer vendor from filename using dynamic config., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., SourceRegistry

### Community 12 - "ConfidenceLevel"
Cohesion: 0.13
Nodes (10): (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor (+2 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.14
Nodes (16): Component, A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, temp_repo(), Create a graph for offline headless synthesis testing., test_graph() (+8 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.07
Nodes (29): LearningEngine, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Load pending deltas from disk. (+21 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.15
Nodes (11): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug. (+3 more)

### Community 19 - "graph.py"
Cohesion: 0.12
Nodes (10): GraphBuilder, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On)., Add a concept and all its attributes as a node in the graph.          Field mapp (+2 more)

### Community 20 - "RuleEngine"
Cohesion: 0.14
Nodes (15): ValidationFailure, ValidationFailureType, GraphBuilder, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates a set of component IDs against the canonical graph to ensure     all c, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules. (+7 more)

### Community 21 - "RepoManager"
Cohesion: 0.13
Nodes (32): BackgroundTasks, FastAPI, ApprovalRequest, approve_delta(), approve_object(), BOQValidationRequest, get_integrations_status(), get_pending_deltas() (+24 more)

### Community 22 - "Platform"
Cohesion: 0.07
Nodes (33): HPEQuickSpecsAdapter, Any, Extract power supply specifications., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende (+25 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.19
Nodes (9): PDFExtractor, Any, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace., Fallback when automated extraction fails or no adapter is found.         Dumps f, get_file_checksum(), ingest_all(), Path (+1 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.10
Nodes (33): Enum, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parses Excel spreadsheets into IKP canonical objects., Source Registry — Registers, classifies, and tracks engineering sources.  Govern, Constraint, DeltaChangeType, EngineeringObjectType (+25 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.40
Nodes (4): IKP Platform State, Knowledge Graph Statistics, Objects by Type, Recent Architecture Changes

### Community 41 - "api.py"
Cohesion: 0.18
Nodes (11): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, lucide-react (+3 more)

### Community 49 - "SourceRegistry"
Cohesion: 0.29
Nodes (4): Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 50 - "Source"
Cohesion: 0.13
Nodes (17): BasePDFAdapter, ABC, Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Extract spatial topology and slot mappings., TableParser (+9 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.19
Nodes (14): _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf, Direct regression test for the specific dedup bug found in the     2026-07-18 au, Walk every Pydantic field on `obj` and confirm it made it into     node_attrs, e, test_category_limit_fields_all_reach_graph() (+6 more)

### Community 52 - "Platform"
Cohesion: 0.25
Nodes (5): datetime, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., _utcnow(), OKF Writer — Writes engineering knowledge objects to disk in Open Knowledge Form, Repository Manager — Orchestrates bidirectional sync between OKF files and the i

### Community 53 - "CustomerRequest"
Cohesion: 0.10
Nodes (29): mock_evaluate(), CustomerRequest, CustomerRequirement, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, Parse natural language into a structured request using LLM. (+21 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.27
Nodes (3): Path, Background watcher that monitors the repository/ directory for external edits, RepositoryWatcher

### Community 55 - "ExcelExtractor"
Cohesion: 0.23
Nodes (5): IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Minimum relationship types from Blueprint 03 §7., RelationshipType, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already

### Community 56 - "conftest.py"
Cohesion: 0.25
Nodes (7): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir()

### Community 57 - ".extract"
Cohesion: 0.33
Nodes (4): DataFrame, Parse a dataframe of components., Parse a dataframe of SKUs., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta).

### Community 58 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 62 - "._read_frontmatter"
Cohesion: 0.33
Nodes (4): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Return graph statistics for observability.

### Community 63 - "mcp_server.py"
Cohesion: 0.14
Nodes (14): cmd_query(), Query the knowledge base with natural language., IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Workflow Nodes — Defines the executable agents and functions for LangGraph.  Gov, # IMPORTANT: Increment attempt_count to avoid infinite loop between validate_bom (+6 more)

### Community 64 - "SourceWatcher"
Cohesion: 0.43
Nodes (6): generate_tree(), main(), parse_python_ast(), parse_typescript_regex(), Extracts class and function signatures from a Python file using AST., Extracts classes and functions from TS/JS using basic regex to save tokens.

### Community 65 - "IKPPlatformUser"
Cohesion: 0.29
Nodes (4): HttpUser, IKPPlatformUser, Simulate frequent simple health checks., Simulate less frequent but heavy BOQ generation requests.

### Community 66 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, lint, preview, test, test:e2e

### Community 70 - ".traverse_relationships"
Cohesion: 0.33
Nodes (3): Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object.

### Community 71 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, type, version

### Community 73 - ".can_handle"
Cohesion: 0.33
Nodes (3): Returns True if this adapter can process the given PDF text., Create a temporary directory for test artifacts., temp_dir()

### Community 75 - "list_tools"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

## Knowledge Gaps
- **97 isolated node(s):** `Recent Architecture Changes`, `Knowledge Graph Statistics`, `Objects by Type`, `name`, `private` (+92 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseEngineeringObject` connect `Source` to `OKFReader`, `IntentParser`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `TestOKFWriter`, `graph.py`, `Platform`, `TestGraphBuilder`, `Platform`, `ExcelExtractor`, `ExcelExtractor`, `.extract`, `test_foundation.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `ConfidenceLevel` to `OKFReader`, `LLMClient`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `Source`, `TestGraphBuilder`, `Platform`, `RepoManager`, `Platform`, `RepositoryWatcher`, `ExcelExtractor`, `TestOKFWriter`, `conftest.py`, `test_foundation.py`, `ExcelExtractor`, `mcp_server.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `graph.py` to `.build_subgraph`, `.traverse_relationships`, `GraphBuilder`, `TestFuzzyMatching`, `Component`, `TestGraphBuilder`, `Source`, `TestOKFWriter`, `CustomerRequest`, `Platform`, `ExcelExtractor`, `conftest.py`, `test_foundation.py`, `._read_frontmatter`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `BaseEngineeringObject`) actually correct?**
  _`HPEQuickSpecsAdapter` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 17 INFERRED edges - model-reasoned connections that need verification._