# Graph Report - vendorsolution_okf  (2026-07-22)

## Corpus Check
- 126 files · ~93,281 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1057 nodes · 2529 edges · 111 communities (74 shown, 37 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 422 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b7d422d4`
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
- RemediationEngine
- rule_engine.py
- .apply_delta
- test_restart_persistence.py
- ikp_shell.sh
- temp_dir
- Enum
- Path
- RepoManager
- SolutionCandidate
- str
- .remove_concept
- Any

## God Nodes (most connected - your core abstractions)
1. `Platform` - 79 edges
2. `HPEQuickSpecsAdapter` - 65 edges
3. `BaseEngineeringObject` - 63 edges
4. `RepoManager` - 58 edges
5. `GraphBuilder` - 57 edges
6. `DeltaChange` - 56 edges
7. `EvidenceRecord` - 55 edges
8. `Component` - 54 edges
9. `EngineeringRelationship` - 51 edges
10. `KnowledgeDelta` - 48 edges

## Surprising Connections (you probably didn't know these)
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOntologyModels` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestRepoManager` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (111 total, 37 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.07
Nodes (44): BaseEngineeringObject, Configuration, Constraint, EngineeringAttribute, LifecycleStatus, Product lifecycle status for engineering objects., Rule severity levels., A typed, structured engineering attribute. (+36 more)

### Community 2 - "LLMClient"
Cohesion: 0.09
Nodes (25): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+17 more)

### Community 3 - "cli.py"
Cohesion: 0.28
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 4 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, jsdom, oxlint, @playwright/test, @testing-library/react, @types/node, @types/react, @types/react-dom (+7 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.19
Nodes (7): Compute SHA-256 hash of a file for duplicate detection., Attempt to infer vendor from filename using dynamic config., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., SourceRegistry, Path

### Community 6 - "GraphBuilder"
Cohesion: 0.10
Nodes (28): CompiledStateGraph, IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent., SolutionGenerator, Workflow Executor — API/CLI entry point for running the LangGraph state machine. (+20 more)

### Community 7 - "App.tsx"
Cohesion: 0.06
Nodes (28): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BomData, CATEGORY_COLORS, categoryColor() (+20 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 9 - "IntentParser"
Cohesion: 0.10
Nodes (16): Client, ComponentSelectionResult, IntentParseResult, KeyManager, LLMClient, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and (+8 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 12 - "ConfidenceLevel"
Cohesion: 0.24
Nodes (7): Any, Computes a stable hash (fingerprint) of all extracted objects' attributes., If the fingerprint changed, we generate targeted DeltaChanges.         If it's t, Phase 5: Tracks extraction fingerprints to generate targeted deltas when a PDF i, VersionTracker, get_file_checksum(), ingest_all()

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.10
Nodes (27): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Extract memory specifications., CategoryLimit, Component, EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve (+19 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.12
Nodes (11): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Load pending deltas from disk., Save a single delta to disk. (+3 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.33
Nodes (4): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Return graph statistics for observability.

### Community 19 - "graph.py"
Cohesion: 0.11
Nodes (10): Any, GraphBuilder, Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Get all outbound dependency targets (Requires, Depends On)., Add a concept and all its attributes as a node in the graph.          Field mapp, Return all components and SKUs for a platform, grouped by category., empty_graph(), Returns a clean GraphBuilder instance. (+2 more)

### Community 21 - "RepoManager"
Cohesion: 0.05
Nodes (42): GraphBuilder, Analyzes validation failures and generates actionable architectural remedies., RemediationEngine, GraphBuilder, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Check if all components are compatible with the platform, enforcing STRICT Solut, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates business rules, constraints, and dependencies against a proposed confi (+34 more)

### Community 22 - "Platform"
Cohesion: 0.10
Nodes (19): Extract power supply specifications., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract spatial topology and slot mappings., Extract storage controller specifications (MR416i, MR216i, NS204i, etc.)., Extract PCIe riser card configurations., Extract internal cable specifications (SAS, power, signal cables)., Extract chassis variants as proper Variant objects.         User note: variants, Extract high-level Workloads (Customer Intent) and link to Platform. (+11 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.17
Nodes (12): PDFExtractor, Any, Fallback when automated extraction fails or no adapter is found.         Dumps f, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace., TableParser, Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source (+4 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.19
Nodes (9): ExcelExtractor, Parses Excel spreadsheets into IKP canonical objects., Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ProcessingStatus, Source classification from Blueprint 04 §3., Source processing lifecycle status., SourceType, TestExcelIngestion (+1 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 31 - "IKP Operations Log"
Cohesion: 0.40
Nodes (4): 2026-07-18, 2026-07-20, 2026-07-22, IKP Operations Log

### Community 41 - "api.py"
Cohesion: 0.18
Nodes (11): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, lucide-react (+3 more)

### Community 49 - "SourceRegistry"
Cohesion: 0.18
Nodes (6): Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 50 - "Source"
Cohesion: 0.22
Nodes (6): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic.

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.17
Nodes (16): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf, Direct regression test for the specific dedup bug found in the     2026-07-18 au (+8 more)

### Community 52 - "Platform"
Cohesion: 0.33
Nodes (3): DiGraph, Check if the BOQ (Bill of Quantities) structure exists entirely within         t, Return an induced subgraph containing only the specified nodes and the         e

### Community 53 - "CustomerRequest"
Cohesion: 0.05
Nodes (47): mock_evaluate(), CustomerRequest, CustomerRequirement, BaseModel, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate (+39 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.31
Nodes (3): Path, Background watcher that monitors the repository/ directory for external edits, RepositoryWatcher

### Community 55 - "ExcelExtractor"
Cohesion: 0.14
Nodes (34): ApprovalRequest, BOQValidationRequest, BaseModel, QueryRequest, SearchRequest, ValidationRequest, apply_feedback(), CorrectionType (+26 more)

### Community 56 - "conftest.py"
Cohesion: 0.25
Nodes (7): api_client(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir(), temp_repo()

### Community 57 - ".extract"
Cohesion: 0.33
Nodes (4): DataFrame, Parse a dataframe of components., Parse a dataframe of SKUs., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta).

### Community 58 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 62 - "._read_frontmatter"
Cohesion: 0.08
Nodes (16): BasePDFAdapter, HPEQuickSpecsAdapter, Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende (+8 more)

### Community 63 - "mcp_server.py"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

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
Cohesion: 0.12
Nodes (16): GraphAnalyticsEngine, Any, GraphBuilder, Graph Analytics Engine — Advanced network analysis for the Knowledge Graph.  Gov, Provides advanced graph algorithms for analyzing the engineering ontology,     s, Find all articulation points (cut vertices) in the knowledge graph.         An a, Generate a report on graph fragility based on articulation points.         Retur, Heuristic "Vendor Solution Match Score" (inspired by Graph Edit Distance). (+8 more)

### Community 70 - ".traverse_relationships"
Cohesion: 0.10
Nodes (13): ObsidianMCPClient, Synchronous wrapper to execute a search against the vault.         Returns a lis, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Check health of the vendor portal / MCP connection.         Returns True if reac, Scrapes the latest data from the vendor portal and creates deltas., Whether the seekstone binary can actually be found on PATH., Any, Build a rich text representation for embedding. More context = better search qua (+5 more)

### Community 71 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, type, version

### Community 72 - "TestFuzzyMatching"
Cohesion: 0.33
Nodes (3): Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object.

### Community 74 - "telemetry_trace"
Cohesion: 0.14
Nodes (24): BackgroundTasks, FastAPI, approve_delta(), approve_object(), get_components(), get_integrations_status(), get_pending_deltas(), get_platform_bom() (+16 more)

### Community 89 - "rule_engine.py"
Cohesion: 0.19
Nodes (13): datetime, Excel Source Parser — Extracts engineering objects from structured spreadsheets., EngineeringObjectType, PackagingType, Enum, str, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Packaging classification for components and SKUs. (+5 more)

## Knowledge Gaps
- **104 isolated node(s):** `2026-07-22`, `2026-07-20`, `2026-07-18`, `Knowledge Graph Statistics`, `Objects by Type` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `graph.py` to `OKFReader`, `LLMClient`, `conftest.py`, `GraphBuilder`, `.traverse_relationships`, `TestFuzzyMatching`, `list_tools`, `.remove_concept`, `Component`, `TestGraphBuilder`, `TestOKFWriter`, `Platform`, `RepoManager`, `CustomerRequest`, `RemediationEngine`, `ExcelExtractor`, `.apply_delta`, `test_restart_persistence.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `OKFReader` to `LLMClient`, `.traverse_relationships`, `IntentParser`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `Source`, `test_graph_field_parity.py`, `graph.py`, `CustomerRequest`, `Platform`, `RepoManager`, `ExcelExtractor`, `rule_engine.py`, `TestGraphBuilder`, `test_foundation.py`, `._read_frontmatter`, `.extract`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `LLMClient` to `OKFReader`, `.traverse_relationships`, `GraphBuilder`, `telemetry_trace`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `SourceRegistry`, `TestGraphBuilder`, `graph.py`, `Platform`, `ExcelExtractor`, `RepositoryWatcher`, `conftest.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BaseEngineeringObject` and `CategoryLimit`) actually correct?**
  _`HPEQuickSpecsAdapter` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 19 INFERRED edges - model-reasoned connections that need verification._