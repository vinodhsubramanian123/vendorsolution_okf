# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 93 files · ~40,599 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 815 nodes · 2089 edges · 70 communities (59 shown, 11 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 391 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4957ce22`
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
- .traverse_relationships
- KnowledgeDelta
- Rule
- SKU
- models.py
- conftest.py
- TableParser
- SourceWatcher
- logger.py
- TestPlatformIdentityAgainstRealPDFs
- ._process_structured_components
- list_tools
- temp_dir

## God Nodes (most connected - your core abstractions)
1. `Platform` - 65 edges
2. `HPEQuickSpecsAdapter` - 64 edges
3. `GraphBuilder` - 64 edges
4. `BaseEngineeringObject` - 63 edges
5. `RepoManager` - 55 edges
6. `EvidenceRecord` - 51 edges
7. `Source` - 42 edges
8. `RuleEngine` - 42 edges
9. `OKFReader` - 42 edges
10. `Component` - 41 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `HPEQuickSpecsAdapter`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/adapters/hpe_quickspecs_adapter.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `HPEQuickSpecsAdapter`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/adapters/hpe_quickspecs_adapter.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestCategoryLimits` --uses--> `RelationshipType`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (70 total, 11 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.11
Nodes (18): PackagingType, Packaging classification for components and SKUs., Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., SolutionCategory, Variant, OKFReader, Any (+10 more)

### Community 1 - "TableParser"
Cohesion: 0.29
Nodes (4): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.09
Nodes (12): LLMClient, Any, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON., Ask Gemini to select the optimal subset of components from a given list that sat (+4 more)

### Community 3 - "cli.py"
Cohesion: 0.20
Nodes (14): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_scan(), cmd_status(), cmd_validate(), main(), IKP CLI — Command-line interface for the Infrastructure Knowledge Platform.  Usa (+6 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.15
Nodes (14): Any, Deterministically validate the drafted BOM using the static RuleEngine., [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., [PLACEHOLDER] - Future Human-In-The-Loop (HITL) step., Traverse HasSKU edges and rank solutions based on business logic., Encapsulates the process nodes for the LangGraph state machine., Parse the unstructured customer message into strict requirements. (+6 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.09
Nodes (15): DiGraph, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, GraphBuilder, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri (+7 more)

### Community 7 - "App.tsx"
Cohesion: 0.09
Nodes (20): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+12 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.14
Nodes (16): Extract power supply specifications., Main extraction entry point.         Returns (list of engineering objects, knowl, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Extract spatial topology and slot mappings., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract storage / drive cage specifications., Extract networking/OCP/NIC information. (+8 more)

### Community 9 - "IntentParser"
Cohesion: 0.40
Nodes (3): CustomerRequirement, A single structured requirement extracted from a customer request., Parse natural language into a structured request using LLM.

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.16
Nodes (14): cmd_query(), Query the knowledge base with natural language., IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent. (+6 more)

### Community 12 - "ConfidenceLevel"
Cohesion: 0.21
Nodes (20): ApprovalRequest, BOQValidationRequest, BaseModel, QueryRequest, SearchRequest, ValidationRequest, LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec (+12 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.16
Nodes (15): Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract memory specifications., CategoryLimit, Component, EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category (+7 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.15
Nodes (11): Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, Merge all validated deltas into the canonical repository.         Returns the nu, BaseEngineeringObject, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Add a concept and all its attributes as a node in the graph.          Field mapp, Repository Manager — Orchestrates bidirectional sync between OKF files and the i, Any, Search the vector database and return a list of matching IDs with confidence sco (+3 more)

### Community 17 - "TestGraphBuilder"
Cohesion: 0.12
Nodes (11): Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, Workload, Builds a single candidate and validates it., Generate multiple solution profiles.         Blueprint 05 §13: Where appropriate, Blueprint 05 §13: Solution must include reasoning and confidence., Create a small test graph with known structure. (+3 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.11
Nodes (14): OKFWriter, Any, Path, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Generate an index.md for the given directory listing all .md concepts.         O, Writes engineering knowledge to disk in OKF format., Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y (+6 more)

### Community 19 - "graph.py"
Cohesion: 0.15
Nodes (13): Decorator for end-to-end observability.     Logs method entry, exit, duration, e, telemetry_trace(), Workflow Executor — API/CLI entry point for running the LangGraph state machine., build_workflow_graph(), Workflow Graph — Defines the LangGraph state machine structure and conditional e, Conditional edge router based on BOM validation with bounded retries., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine. (+5 more)

### Community 20 - "RuleEngine"
Cohesion: 0.16
Nodes (9): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates a set of component IDs against the canonical graph to ensure     all c, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine, Any (+1 more)

### Community 21 - "RepoManager"
Cohesion: 0.11
Nodes (12): (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, Load all existing OKF files into the in-memory graph.         Returns the number (+4 more)

### Community 22 - "Platform"
Cohesion: 0.12
Nodes (11): HPEQuickSpecsAdapter, Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does (+3 more)

### Community 23 - "api.py"
Cohesion: 0.24
Nodes (13): FastAPI, approve_object(), get_repo(), get_review_queue(), get_status(), _infer_platforms_for_components(), lifespan(), query_solution() (+5 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.21
Nodes (8): DataFrame, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., TestExcelIngestion

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.17
Nodes (20): Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, EngineeringObjectType, LifecycleStatus, ProcessingStatus, Product lifecycle status for engineering objects., Rule severity levels., Canonical hierarchy levels from Blueprint 03 §3. (+12 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "api.py"
Cohesion: 0.16
Nodes (14): BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, ABC, BaseModel, Vendor Validation — Abstract interface for vendor validation integration.  Gover, A single message from a validation check., Complete result of validating a solution candidate.     Blueprint 06 §9: Portal (+6 more)

### Community 49 - "SourceRegistry"
Cohesion: 0.22
Nodes (7): Path, Compute SHA-256 hash of a file for duplicate detection., Attempt to infer vendor from filename., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., SourceRegistry

### Community 50 - "Source"
Cohesion: 0.22
Nodes (11): PDFExtractor, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace., Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source, get_file_checksum(), ingest_all(), Path (+3 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.23
Nodes (12): _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf, Walk every Pydantic field on `obj` and confirm it made it into     node_attrs, e, test_category_limit_fields_all_reach_graph(), test_component_fields_all_reach_graph() (+4 more)

### Community 52 - "Platform"
Cohesion: 0.23
Nodes (8): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050).

### Community 53 - "CustomerRequest"
Cohesion: 0.33
Nodes (4): Any, Executes customer queries against the LangGraph orchestrator., Run a user query through the end-to-end multi-step pipeline., WorkflowExecutor

### Community 54 - ".traverse_relationships"
Cohesion: 0.20
Nodes (6): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object.

### Community 55 - "KnowledgeDelta"
Cohesion: 0.22
Nodes (6): Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, KnowledgeDelta, Every newly acquired engineering source produces a Knowledge Delta.     Blueprin, Blueprint 02 §7: Knowledge Delta with changes list.

### Community 56 - "Rule"
Cohesion: 0.22
Nodes (7): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, Blueprint 03 §8: Rule must expose scope, confidence, evidence, version., Direct regression test for the specific dedup bug found in the     2026-07-18 au, test_platform_id_survives_for_rule_dedup(), Test that relationships (edges) and body contents survive a restart/roundtrip., test_okf_persistence_roundtrip()

### Community 57 - "SKU"
Cohesion: 0.32
Nodes (3): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, TestFuzzyMatching

### Community 58 - "models.py"
Cohesion: 0.15
Nodes (15): datetime, Configuration, Constraint, HistoryEntry, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., Spatial topology mapping for physical components. (+7 more)

### Community 62 - "conftest.py"
Cohesion: 0.25
Nodes (7): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir()

### Community 63 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Fallback when automated extraction fails or no adapter is found.         Dumps f, TableParser

### Community 64 - "SourceWatcher"
Cohesion: 0.29
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 65 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 67 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

### Community 68 - "list_tools"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

## Knowledge Gaps
- **88 isolated node(s):** `Solution Domains`, `Sources Ingested: 1`, `Learnings & Architecture Updates (Agent Run)`, `1. Add `tools/` to your PATH`, `2. Frontend (ikp_web)` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `LLMClient`, `WorkflowNodes`, `api.py`, `SolutionGenerator`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `TestOKFWriter`, `graph.py`, `RuleEngine`, `RepoManager`, `.traverse_relationships`, `CustomerRequest`, `SKU`, `test_foundation.py`, `conftest.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `BaseEngineeringObject` to `OKFReader`, `TableParser`, `GraphBuilder`, `EvidenceRecord`, `ConfidenceLevel`, `Component`, `TestGraphBuilder`, `TestOKFWriter`, `RepoManager`, `Platform`, `ExcelExtractor`, `test_foundation.py`, `Source`, `Platform`, `Rule`, `SKU`, `models.py`, `TableParser`, `._process_structured_components`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `HPEQuickSpecsAdapter` connect `Platform` to `OKFReader`, `TableParser`, `LLMClient`, `._process_structured_components`, `TestPlatformIdentityAgainstRealPDFs`, `EvidenceRecord`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `Source`, `Platform`, `KnowledgeDelta`, `Rule`, `SKU`, `models.py`, `test_foundation.py`, `TableParser`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `TableParser`) actually correct?**
  _`HPEQuickSpecsAdapter` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._