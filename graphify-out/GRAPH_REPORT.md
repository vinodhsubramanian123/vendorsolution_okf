# Graph Report - vendorsolution_okf  (2026-07-20)

## Corpus Check
- 112 files · ~49,425 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 987 nodes · 2423 edges · 88 communities (65 shown, 23 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 418 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b7a63f3e`
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
- VendorValidator

## God Nodes (most connected - your core abstractions)
1. `Platform` - 75 edges
2. `BaseEngineeringObject` - 62 edges
3. `HPEQuickSpecsAdapter` - 59 edges
4. `RuleEngine` - 56 edges
5. `EvidenceRecord` - 51 edges
6. `Component` - 51 edges
7. `GraphBuilder` - 49 edges
8. `EngineeringRelationship` - 47 edges
9. `RepoManager` - 46 edges
10. `Source` - 42 edges

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

## Communities (88 total, 23 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.10
Nodes (37): Configuration, Constraint, EngineeringAttribute, EngineeringObjectType, LifecycleStatus, Product lifecycle status for engineering objects., A typed, structured engineering attribute., Canonical hierarchy levels from Blueprint 03 §3. (+29 more)

### Community 2 - "LLMClient"
Cohesion: 0.18
Nodes (16): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+8 more)

### Community 3 - "cli.py"
Cohesion: 0.28
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 4 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, jsdom, oxlint, @playwright/test, @testing-library/react, @types/node, @types/react, @types/react-dom (+7 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.17
Nodes (12): Any, Deterministically validate the drafted BOM using the static RuleEngine., Dynamically recover from validation failures.         1. Try next candidate in r, Encapsulates the process nodes for the LangGraph state machine., [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., Aggregate validation errors and portal rejections into a full-solution FailureRe, Traverse HasSKU edges and rank solutions based on business logic and track delta (+4 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.15
Nodes (17): CompiledStateGraph, Decorator for end-to-end observability.     Logs method entry, exit, duration, e, telemetry_trace(), Workflow Executor — API/CLI entry point for running the LangGraph state machine., build_workflow_graph(), Workflow Graph — Defines the LangGraph state machine structure and conditional e, Conditional edge router based on BOM validation with bounded retries., Conditional edge router after select_recovery_strategy. (+9 more)

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

### Community 12 - "ConfidenceLevel"
Cohesion: 0.14
Nodes (8): (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, main(), Rebuilds the semantic (vector) search index from everything already in repositor

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.16
Nodes (15): Component, Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, Create a graph for offline headless synthesis testing., test_graph(), Create a graph for chaos testing., test_graph() (+7 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.12
Nodes (11): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Load pending deltas from disk., Save a single delta to disk. (+3 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.13
Nodes (13): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug. (+5 more)

### Community 19 - "graph.py"
Cohesion: 0.09
Nodes (16): GraphBuilder, Any, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri (+8 more)

### Community 20 - "RuleEngine"
Cohesion: 0.14
Nodes (13): GraphBuilder, Check if all components are compatible with the platform, enforcing STRICT Solut, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates business rules, constraints, and dependencies against a proposed confi, Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., RuleEngine (+5 more)

### Community 21 - "RepoManager"
Cohesion: 0.05
Nodes (71): BackgroundTasks, FastAPI, ApprovalRequest, approve_delta(), approve_object(), BOQValidationRequest, get_integrations_status(), get_pending_deltas() (+63 more)

### Community 22 - "Platform"
Cohesion: 0.09
Nodes (22): BasePDFAdapter, HPEQuickSpecsAdapter, Any, Extract power supply specifications., Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard (+14 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.08
Nodes (24): PDFExtractor, Any, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace., Fallback when automated extraction fails or no adapter is found.         Dumps f, TableParser, Compute SHA-256 hash of a file for duplicate detection., Attempt to infer vendor from filename using dynamic config. (+16 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.16
Nodes (18): Enum, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ConfidenceLevel, DeltaChangeType, PackagingType, ProcessingStatus, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr (+10 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 31 - "IKP Operations Log"
Cohesion: 0.50
Nodes (3): 2026-07-18, 2026-07-20, IKP Operations Log

### Community 41 - "api.py"
Cohesion: 0.18
Nodes (11): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, lucide-react (+3 more)

### Community 49 - "SourceRegistry"
Cohesion: 0.29
Nodes (4): Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 50 - "Source"
Cohesion: 0.22
Nodes (6): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic.

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.19
Nodes (14): _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf, Direct regression test for the specific dedup bug found in the     2026-07-18 au, Walk every Pydantic field on `obj` and confirm it made it into     node_attrs, e, test_category_limit_fields_all_reach_graph() (+6 more)

### Community 52 - "Platform"
Cohesion: 0.13
Nodes (11): datetime, BaseEngineeringObject, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, _utcnow(), Path, Split an OKF file into (frontmatter_dict, body_str)., Recursively scan the repository and parse all concept files.         Skips reser (+3 more)

### Community 53 - "CustomerRequest"
Cohesion: 0.12
Nodes (19): CustomerRequest, CustomerRequirement, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, Parse natural language into a structured request using LLM., Builds a single candidate and validates it., Generate multiple solution profiles.         Blueprint 05 §13: Where appropriate, Draft a Bill of Materials based on platform compatibility using LLM and constrai (+11 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.27
Nodes (3): Path, Background watcher that monitors the repository/ directory for external edits, RepositoryWatcher

### Community 55 - "ExcelExtractor"
Cohesion: 0.16
Nodes (9): Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., CategoryLimit, A constraint specifically targeting a maximum or minimum quantity for a category, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already, mock_graph(), test_dynamic_math_exhaustion(), test_missing_dependency_failure() (+1 more)

### Community 56 - "conftest.py"
Cohesion: 0.20
Nodes (9): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir() (+1 more)

### Community 57 - ".extract"
Cohesion: 0.21
Nodes (9): DataFrame, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU (+1 more)

### Community 58 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 62 - "._read_frontmatter"
Cohesion: 0.13
Nodes (6): Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does, Extract the main platform identity from the document using generalized heuristic

### Community 63 - "mcp_server.py"
Cohesion: 0.18
Nodes (13): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent., SolutionGenerator, Workflow Nodes — Defines the executable agents and functions for LangGraph.  Gov, # IMPORTANT: Increment attempt_count to avoid infinite loop between validate_bom (+5 more)

### Community 64 - "SourceWatcher"
Cohesion: 0.43
Nodes (6): generate_tree(), main(), parse_python_ast(), parse_typescript_regex(), Extracts class and function signatures from a Python file using AST., Extracts classes and functions from TS/JS using basic regex to save tokens.

### Community 65 - "IKPPlatformUser"
Cohesion: 0.29
Nodes (4): HttpUser, IKPPlatformUser, Simulate frequent simple health checks., Simulate less frequent but heavy BOQ generation requests.

### Community 66 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, dev, lint, preview, test, test:e2e

### Community 67 - ".build_subgraph"
Cohesion: 0.09
Nodes (19): DiGraph, GraphAnalyticsEngine, Any, GraphBuilder, Graph Analytics Engine — Advanced network analysis for the Knowledge Graph.  Gov, Provides advanced graph algorithms for analyzing the engineering ontology,     s, Find all articulation points (cut vertices) in the knowledge graph.         An a, Generate a report on graph fragility based on articulation points.         Retur (+11 more)

### Community 69 - "TestPlatformIdentityAgainstRealPDFs"
Cohesion: 0.18
Nodes (9): mock_evaluate(), Any, Executes customer queries against the LangGraph orchestrator., Run a user query through the end-to-end multi-step pipeline., WorkflowExecutor, Test that the orchestrator respects max_attempts (3) when failures are unique (n, test_exhaustion_limits(), Test the LangGraph pipeline from intent to ranked solutions. (+1 more)

### Community 70 - ".traverse_relationships"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Synchronous wrapper to execute a search against the vault.         Returns a lis, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH.

### Community 71 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, type, version

### Community 72 - "TestFuzzyMatching"
Cohesion: 0.60
Nodes (3): Spatial topology mapping for physical components., SlotMapping, TestTopology

### Community 75 - "list_tools"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

## Knowledge Gaps
- **98 isolated node(s):** `2026-07-20`, `2026-07-18`, `Knowledge Graph Statistics`, `Objects by Type`, `ChatMessage` (+93 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseEngineeringObject` connect `Platform` to `OKFReader`, `TestFuzzyMatching`, `IntentParser`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `Source`, `TestOKFWriter`, `graph.py`, `RepoManager`, `Platform`, `ExcelExtractor`, `ExcelExtractor`, `.extract`, `TestGraphBuilder`, `test_foundation.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `graph.py` to `OKFReader`, `.build_subgraph`, `TestPlatformIdentityAgainstRealPDFs`, `GraphBuilder`, `Component`, `TestGraphBuilder`, `TestOKFWriter`, `Platform`, `RepoManager`, `ExcelExtractor`, `conftest.py`, `ExcelExtractor`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `ConfidenceLevel` to `OKFReader`, `LLMClient`, `BaseEngineeringObject`, `SourceRegistry`, `TestGraphBuilder`, `TestOKFWriter`, `Platform`, `RepoManager`, `Platform`, `RepositoryWatcher`, `ExcelExtractor`, `conftest.py`, `test_foundation.py`, `mcp_server.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BaseEngineeringObject` and `CategoryLimit`) actually correct?**
  _`HPEQuickSpecsAdapter` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `RuleEngine` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RuleEngine` has 16 INFERRED edges - model-reasoned connections that need verification._