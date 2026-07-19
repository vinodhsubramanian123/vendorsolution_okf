# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 95 files · ~42,732 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 844 nodes · 2140 edges · 63 communities (51 shown, 12 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 392 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cc9532d6`
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
- Source
- test_graph_field_parity.py
- Platform
- CustomerRequest
- Rule
- models.py
- SourceWatcher
- logger.py
- TestPlatformIdentityAgainstRealPDFs
- ._process_structured_components
- temp_dir

## God Nodes (most connected - your core abstractions)
1. `Platform` - 65 edges
2. `GraphBuilder` - 64 edges
3. `BaseEngineeringObject` - 62 edges
4. `HPEQuickSpecsAdapter` - 61 edges
5. `RepoManager` - 56 edges
6. `EvidenceRecord` - 51 edges
7. `Source` - 42 edges
8. `DeltaChange` - 42 edges
9. `RuleEngine` - 42 edges
10. `OKFReader` - 42 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `HPEQuickSpecsAdapter`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/adapters/hpe_quickspecs_adapter.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `HPEQuickSpecsAdapter`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/adapters/hpe_quickspecs_adapter.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (63 total, 12 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.13
Nodes (15): Configuration, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, Variant, OKFReader, Any, Path, Helper to build a Pydantic object from frontmatter and body. (+7 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Synchronous wrapper to execute a search against the vault.         Returns a lis, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH.

### Community 3 - "cli.py"
Cohesion: 0.18
Nodes (16): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+8 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.15
Nodes (14): Any, Deterministically validate the drafted BOM using the static RuleEngine., [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., [PLACEHOLDER] - Future Human-In-The-Loop (HITL) step., Traverse HasSKU edges and rank solutions based on business logic., Encapsulates the process nodes for the LangGraph state machine., Parse the unstructured customer message into strict requirements. (+6 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.07
Nodes (19): DiGraph, GraphBuilder, Any, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria. (+11 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (27): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+19 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.12
Nodes (16): Extract power supply specifications., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract spatial topology and slot mappings., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract memory specifications., Extract storage / drive cage specifications., Extract networking/OCP/NIC information. (+8 more)

### Community 9 - "IntentParser"
Cohesion: 0.10
Nodes (14): Client, ComponentSelectionResult, IntentParseResult, KeyManager, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Ask Gemini to select the optimal subset of components from a given list that sat (+6 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.12
Nodes (17): IntentParser, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., LLMClient, Wrapper for the Gemini LLM API., Any, Generates explainable solution candidates based on customer intent., SolutionGenerator (+9 more)

### Community 12 - "ConfidenceLevel"
Cohesion: 0.18
Nodes (7): Repository Manager — Orchestrates bidirectional sync between OKF files and the i, (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.10
Nodes (26): Excel Source Parser — Extracts engineering objects from structured spreadsheets., CategoryLimit, Component, EngineeringRelationship, PackagingType, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Packaging classification for components and SKUs., A directed, typed, evidence-backed relationship between two engineering objects. (+18 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.22
Nodes (5): Any, Search the vector database and return a list of matching IDs with confidence sco, Vectorize and index a single object. Prefer index_many() for         bulk ingest, Vectorize and index a list of objects, batching embedding API         calls in g, VectorStore

### Community 18 - "TestOKFWriter"
Cohesion: 0.11
Nodes (14): OKFWriter, Any, Path, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Generate an index.md for the given directory listing all .md concepts.         O, Writes engineering knowledge to disk in OKF format., Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y (+6 more)

### Community 19 - "graph.py"
Cohesion: 0.14
Nodes (16): Decorator for end-to-end observability.     Logs method entry, exit, duration, e, telemetry_trace(), Intent Parser — Extracts structured engineering requirements from natural langua, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluates a set of component IDs against the canonical graph to ensure     all c, RuleEngine, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov (+8 more)

### Community 20 - "RuleEngine"
Cohesion: 0.20
Nodes (5): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut

### Community 21 - "RepoManager"
Cohesion: 0.18
Nodes (6): Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 22 - "Platform"
Cohesion: 0.11
Nodes (12): HPEQuickSpecsAdapter, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags. (+4 more)

### Community 23 - "api.py"
Cohesion: 0.29
Nodes (7): CompiledStateGraph, build_workflow_graph(), Conditional edge router based on BOM validation with bounded retries., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine., should_human_intervene(), should_loop_bom()

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.17
Nodes (22): Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, Constraint, EngineeringObjectType, LifecycleStatus, ProcessingStatus, Product lifecycle status for engineering objects., Rule severity levels. (+14 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "api.py"
Cohesion: 0.05
Nodes (66): FastAPI, ApprovalRequest, approve_delta(), approve_object(), BOQValidationRequest, get_integrations_status(), get_pending_deltas(), get_repo() (+58 more)

### Community 50 - "Source"
Cohesion: 0.07
Nodes (27): DataFrame, ExcelExtractor, Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., PDFExtractor, Any, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace. (+19 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.12
Nodes (21): Parse a dataframe of components., EngineeringAttribute, A typed, structured engineering attribute., Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field. (+13 more)

### Community 52 - "Platform"
Cohesion: 0.14
Nodes (14): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, BaseEngineeringObject (+6 more)

### Community 53 - "CustomerRequest"
Cohesion: 0.16
Nodes (10): CustomerRequest, Structured customer engineering request.     Blueprint 05 §4: Customer requests, Builds a single candidate and validates it., Generate multiple solution profiles.         Blueprint 05 §13: Where appropriate, Any, Executes customer queries against the LangGraph orchestrator., Run a user query through the end-to-end multi-step pipeline., WorkflowExecutor (+2 more)

### Community 56 - "Rule"
Cohesion: 0.25
Nodes (6): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, OKF Writer — Writes engineering knowledge objects to disk in Open Knowledge Form, Blueprint 03 §8: Rule must expose scope, confidence, evidence, version., Direct regression test for the specific dedup bug found in the     2026-07-18 au, test_platform_id_survives_for_rule_dedup()

### Community 58 - "models.py"
Cohesion: 0.67
Nodes (3): datetime, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., _utcnow()

### Community 64 - "SourceWatcher"
Cohesion: 0.29
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 65 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 67 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

## Knowledge Gaps
- **90 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `WorkflowNodes`, `api.py`, `SolutionGenerator`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `TestOKFWriter`, `graph.py`, `Platform`, `CustomerRequest`, `test_graph_field_parity.py`, `api.py`, `test_foundation.py`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `Platform` to `OKFReader`, `._process_structured_components`, `GraphBuilder`, `EvidenceRecord`, `api.py`, `IntentParser`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `Source`, `test_graph_field_parity.py`, `graph.py`, `TestOKFWriter`, `Platform`, `RepoManager`, `Rule`, `test_foundation.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `ConfidenceLevel` to `OKFReader`, `LLMClient`, `cli.py`, `GraphBuilder`, `EvidenceRecord`, `api.py`, `SolutionGenerator`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `TestOKFWriter`, `Source`, `Platform`, `RepoManager`, `test_foundation.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `BaseEngineeringObject`) actually correct?**
  _`HPEQuickSpecsAdapter` has 27 INFERRED edges - model-reasoned connections that need verification._