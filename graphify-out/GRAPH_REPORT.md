# Graph Report - vendorsolution_okf  (2026-07-20)

## Corpus Check
- 100 files · ~45,636 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 890 nodes · 2297 edges · 66 communities (55 shown, 11 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 425 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6549b3e8`
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
- .extract
- logger.py
- ._read_frontmatter
- mcp_server.py
- SourceWatcher
- .build_subgraph

## God Nodes (most connected - your core abstractions)
1. `Platform` - 69 edges
2. `GraphBuilder` - 69 edges
3. `BaseEngineeringObject` - 62 edges
4. `HPEQuickSpecsAdapter` - 61 edges
5. `RepoManager` - 59 edges
6. `EvidenceRecord` - 51 edges
7. `Component` - 45 edges
8. `RuleEngine` - 44 edges
9. `EngineeringRelationship` - 43 edges
10. `Source` - 42 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `HPEQuickSpecsAdapter`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/adapters/hpe_quickspecs_adapter.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestCategoryLimits` --uses--> `RelationshipType`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (66 total, 11 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.09
Nodes (15): Configuration, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, SolutionCategory, Variant, Any, Path (+7 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.18
Nodes (16): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+8 more)

### Community 3 - "cli.py"
Cohesion: 0.28
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.12
Nodes (17): Any, Run a user query through the end-to-end multi-step pipeline., Any, Deterministically validate the drafted BOM using the static RuleEngine., Dynamically recover from validation failures.         1. Try next candidate in r, Encapsulates the process nodes for the LangGraph state machine., [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop. (+9 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.20
Nodes (9): CompiledStateGraph, build_workflow_graph(), Conditional edge router based on BOM validation with bounded retries., Conditional edge router after select_recovery_strategy., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine., route_recovery(), should_human_intervene() (+1 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (28): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+20 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 9 - "IntentParser"
Cohesion: 0.08
Nodes (21): Client, ComponentSelectionResult, IntentParseResult, KeyManager, LLMClient, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and (+13 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.23
Nodes (7): Path, Compute SHA-256 hash of a file for duplicate detection., Attempt to infer vendor from filename using dynamic config., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., SourceRegistry

### Community 12 - "ConfidenceLevel"
Cohesion: 0.19
Nodes (7): Repository Manager — Orchestrates bidirectional sync between OKF files and the i, (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.11
Nodes (22): Extract power supply specifications., Excel Source Parser — Extracts engineering objects from structured spreadsheets., Component, EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload (+14 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.10
Nodes (16): Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., LearningEngine, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t (+8 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.18
Nodes (8): OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re, TestOKFWriter

### Community 19 - "graph.py"
Cohesion: 0.08
Nodes (22): Decorator for end-to-end observability.     Logs method entry, exit, duration, e, telemetry_trace(), Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, GraphBuilder, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities. (+14 more)

### Community 20 - "RuleEngine"
Cohesion: 0.13
Nodes (9): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates a set of component IDs against the canonical graph to ensure     all c, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine, Any (+1 more)

### Community 21 - "RepoManager"
Cohesion: 0.22
Nodes (16): BackgroundTasks, approve_delta(), approve_object(), get_integrations_status(), get_pending_deltas(), get_repo(), get_review_queue(), get_status() (+8 more)

### Community 22 - "Platform"
Cohesion: 0.05
Nodes (31): HPEQuickSpecsAdapter, Classify a component description into (category, subcategory) using keyword scor, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract spatial topology and slot mappings., Extract product description from introductory text., Extract chassis type variants. (+23 more)

### Community 23 - "api.py"
Cohesion: 0.15
Nodes (14): BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, ABC, BaseModel, Vendor Validation — Abstract interface for vendor validation integration.  Gover, A single message from a validation check., Complete result of validating a solution candidate.     Blueprint 06 §9: Portal (+6 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.15
Nodes (9): Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract memory specifications., Extract storage / drive cage specifications., Extract networking/OCP/NIC information., Extract GPU/accelerator information., DeltaChange (+1 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.11
Nodes (22): datetime, Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, PackagingType, ProcessingStatus, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Rule severity levels., Packaging classification for components and SKUs. (+14 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.40
Nodes (4): IKP Platform State, Knowledge Graph Statistics, Objects by Type, Recent Architecture Changes

### Community 41 - "api.py"
Cohesion: 0.31
Nodes (16): ApprovalRequest, BOQValidationRequest, BaseModel, QueryRequest, SearchRequest, ValidationRequest, DeltaChangeType, DeltaStatus (+8 more)

### Community 49 - "SourceRegistry"
Cohesion: 0.18
Nodes (6): Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 50 - "Source"
Cohesion: 0.15
Nodes (14): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, BaseEngineeringObject (+6 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.12
Nodes (20): Any, Convert structured dictionary rows from TableParser into Component + SKU objects, CategoryLimit, EngineeringAttribute, A typed, structured engineering attribute., A constraint specifically targeting a maximum or minimum quantity for a category, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo (+12 more)

### Community 52 - "Platform"
Cohesion: 0.24
Nodes (4): ObsidianMCPClient, Synchronous wrapper to execute a search against the vault.         Returns a lis, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH.

### Community 53 - "CustomerRequest"
Cohesion: 0.13
Nodes (26): mock_evaluate(), CustomerRequest, CustomerRequirement, BaseModel, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, ValidationFailure, ValidationFailureType (+18 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.24
Nodes (5): FastAPI, lifespan(), Path, Background watcher that monitors the repository/ directory for external edits, RepositoryWatcher

### Community 55 - "ExcelExtractor"
Cohesion: 0.16
Nodes (24): ConfidenceLevel, Constraint, EngineeringObjectType, LifecycleStatus, Product lifecycle status for engineering objects., Confidence levels for extracted knowledge., Canonical hierarchy levels from Blueprint 03 §3., An engineering limitation (max controllers, max drives, max memory, etc.).     B (+16 more)

### Community 57 - ".extract"
Cohesion: 0.15
Nodes (9): DataFrame, ExcelExtractor, Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, TestExcelIngestion (+1 more)

### Community 58 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 62 - "._read_frontmatter"
Cohesion: 0.17
Nodes (7): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object., Return graph statistics for observability.

### Community 63 - "mcp_server.py"
Cohesion: 0.16
Nodes (14): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Generates explainable solution candidates based on customer intent., SolutionGenerator, call_tool(), get_repo(), list_tools() (+6 more)

### Community 64 - "SourceWatcher"
Cohesion: 0.43
Nodes (6): generate_tree(), main(), parse_python_ast(), parse_typescript_regex(), Extracts class and function signatures from a Python file using AST., Extracts classes and functions from TS/JS using basic regex to save tokens.

## Knowledge Gaps
- **90 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `graph.py` to `.build_subgraph`, `WorkflowNodes`, `GraphBuilder`, `ConfidenceLevel`, `Component`, `TestGraphBuilder`, `Source`, `test_graph_field_parity.py`, `RuleEngine`, `Platform`, `api.py`, `ExcelExtractor`, `CustomerRequest`, `Platform`, `TestOKFWriter`, `.extract`, `._read_frontmatter`, `mcp_server.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `ConfidenceLevel` to `LLMClient`, `api.py`, `IntentParser`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `Source`, `graph.py`, `Platform`, `RepoManager`, `RepositoryWatcher`, `ExcelExtractor`, `TestOKFWriter`, `Platform`, `TestGraphBuilder`, `test_foundation.py`, `mcp_server.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `Source` to `OKFReader`, `IntentParser`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `TestOKFWriter`, `test_graph_field_parity.py`, `graph.py`, `CustomerRequest`, `Platform`, `ExcelExtractor`, `ExcelExtractor`, `.extract`, `TestGraphBuilder`, `test_foundation.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `BaseEngineeringObject`) actually correct?**
  _`HPEQuickSpecsAdapter` has 27 INFERRED edges - model-reasoned connections that need verification._