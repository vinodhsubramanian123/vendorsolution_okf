# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 91 files · ~38,141 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 795 nodes · 1763 edges · 65 communities (53 shown, 12 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 290 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4ac581f8`
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
- BaseModel
- Path

## God Nodes (most connected - your core abstractions)
1. `GraphBuilder` - 62 edges
2. `RepoManager` - 44 edges
3. `OKFReader` - 43 edges
4. `PDFExtractor` - 42 edges
5. `TestGraphBuilder` - 41 edges
6. `RuleEngine` - 40 edges
7. `BaseEngineeringObject` - 40 edges
8. `Platform` - 38 edges
9. `Source` - 34 edges
10. `TestOntologyModels` - 34 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestCategoryLimits` --uses--> `RuleEngine`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/reasoning/rule_engine.py
- `TestCategoryLimits` --uses--> `GraphBuilder`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/repository/graph_builder.py
- `TestGraphBuilder` --uses--> `GraphBuilder`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/repository/graph_builder.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (65 total, 12 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.10
Nodes (24): BaseEngineeringObject, Configuration, Constraint, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, An engineering limitation (max controllers, max drives, max memory, etc.).     B, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame'). (+16 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.11
Nodes (21): ABC, DeltaChange, A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, A single change within a Knowledge Delta., SKU, BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched (+13 more)

### Community 2 - "IntentParser"
Cohesion: 0.08
Nodes (18): IntentParser, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from (+10 more)

### Community 3 - "RepoManager"
Cohesion: 0.09
Nodes (26): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+18 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "Component"
Cohesion: 0.16
Nodes (14): Any, [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., [PLACEHOLDER] - Future Human-In-The-Loop (HITL) step., Traverse HasSKU edges and rank solutions based on business logic., Encapsulates the process nodes for the LangGraph state machine., Parse the unstructured customer message into strict requirements., Select a platform that Supports the chosen workload. (+6 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.11
Nodes (10): GraphBuilder, BaseEngineeringObject, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On). (+2 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (15): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, KnowledgeTransfer(), Sidebar(), SidebarProps (+7 more)

### Community 8 - "models.py"
Cohesion: 0.21
Nodes (7): Intent Parser — Extracts structured engineering requirements from natural langua, Any, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent., SolutionGenerator, test_rule_engine(), test_solution_generator()

### Community 9 - "cli.py"
Cohesion: 0.28
Nodes (7): call_tool(), get_repo(), list_tools(), RepoManager, List available tools., TextContent, Tool

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.24
Nodes (6): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already, Workflow Nodes — Defines the executable agents and functions for LangGraph.  Gov, main(), main()

### Community 12 - "RuleEngine"
Cohesion: 0.16
Nodes (9): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluates a set of component IDs against the canonical graph to ensure     all c, Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine, IntentParser (+1 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 15 - "._extract_platform_identity"
Cohesion: 0.33
Nodes (3): Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract engineering rules from notes, warnings, and constraints.

### Community 16 - "Platform"
Cohesion: 0.11
Nodes (13): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu (+5 more)

### Community 18 - "SourceRegistry"
Cohesion: 0.06
Nodes (34): DataFrame, ExcelExtractor, Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Path (+26 more)

### Community 19 - "Platform"
Cohesion: 0.12
Nodes (12): Any, BaseEngineeringObject, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file., Derive hierarchical file path from the object's ontological position.          B (+4 more)

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis

### Community 21 - "LearningEngine"
Cohesion: 0.11
Nodes (12): (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, Load all existing OKF files into the in-memory graph.         Returns the number (+4 more)

### Community 22 - "SKU"
Cohesion: 0.13
Nodes (16): CategoryLimit, Component, Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category, api_client(), empty_graph() (+8 more)

### Community 23 - "BOQValidator"
Cohesion: 0.18
Nodes (17): Enum, DeltaChangeType, DeltaStatus, EngineeringObjectType, LifecycleStatus, PackagingType, Product lifecycle status for engineering objects., Knowledge Delta lifecycle status. (+9 more)

### Community 24 - "Component"
Cohesion: 0.17
Nodes (11): Component, Extract spatial topology and slot mappings., Extract processor specifications from QuickSpecs tables., Extract networking/OCP/NIC information., Extract GPU/accelerator information., Extract power supply specifications., Platform, Regression test for the direction-assumption bug found alongside the     field-p (+3 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - ".filter_by_metadata"
Cohesion: 0.14
Nodes (14): CustomerRequest, CustomerRequirement, EngineeringAttribute, HistoryEntry, BaseModel, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, A typed, structured engineering attribute., A single structured requirement extracted from a customer request. (+6 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "__init__.py"
Cohesion: 0.16
Nodes (21): BaseModel, FastAPI, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status() (+13 more)

### Community 49 - "SlotMapping"
Cohesion: 0.13
Nodes (24): datetime, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, ConfidenceLevel, EngineeringRelationship, EvidenceRecord, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Confidence levels for extracted knowledge. (+16 more)

### Community 50 - "BaseEngineeringObject"
Cohesion: 0.18
Nodes (8): PDFExtractor, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does, Extract the main platform identity from the document using generalized heuristic, Extracts engineering knowledge from vendor QuickSpecs and technical PDFs.      B

### Community 51 - "._compute_path"
Cohesion: 0.21
Nodes (13): Rule, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Direct regression test for the specific dedup bug found in the     2026-07-18 au, Walk every Pydantic field on `obj` and confirm it made it into     node_attrs, e, test_category_limit_fields_all_reach_graph() (+5 more)

### Community 52 - "SourceWatcher"
Cohesion: 0.22
Nodes (6): BaseEngineeringObject, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract memory specifications., Extract storage / drive cage specifications., Main extraction entry point.         Returns (list of engineering objects, knowl

### Community 53 - "build_workflow_graph"
Cohesion: 0.11
Nodes (18): Any, Workflow Executor — API/CLI entry point for running the LangGraph state machine., Executes customer queries against the LangGraph orchestrator., Run a user query through the end-to-end multi-step pipeline., WorkflowExecutor, build_workflow_graph(), IntentParser, SolutionGenerator (+10 more)

### Community 54 - "shared_temp_dir"
Cohesion: 0.20
Nodes (6): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges., Get all objects compatible with the given object.

### Community 55 - "temp_dir"
Cohesion: 0.43
Nodes (3): OKFWriter, Writes engineering knowledge to disk in OKF format., TestOKFWriter

### Community 56 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

### Community 57 - ".semantic_search"
Cohesion: 0.40
Nodes (4): Extract high-level Workloads (Customer Intent) and link to Platform., Workload requirements are flattened rather than kept as nested dicts     -- conf, test_workload_requirement_dicts_flatten_into_graph(), Workload

### Community 58 - ".execute_query"
Cohesion: 0.60
Nodes (3): Spatial topology mapping for physical components., SlotMapping, TestTopology

## Knowledge Gaps
- **87 isolated node(s):** `Solution Domains`, `Sources Ingested: 1`, `Learnings & Architecture Updates (Agent Run)`, `Knowledge Graph Statistics`, `Objects by Type` (+82 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `EvidenceRecord`, `Component`, `models.py`, `PDFExtractor`, `RuleEngine`, `Platform`, `SlotMapping`, `TestGraphBuilder`, `._compute_path`, `BOQValidator`, `LearningEngine`, `shared_temp_dir`, `build_workflow_graph`, `SKU`, `temp_dir`, `Component`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `PDFExtractor` connect `BaseEngineeringObject` to `RepoManager`, `PDFExtractor`, `._extract_platform_identity`, `SourceRegistry`, `Platform`, `SourceWatcher`, `._process_structured_components`, `Component`, `.semantic_search`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `LearningEngine` to `BaseEngineeringObject`, `IntentParser`, `RepoManager`, `GraphBuilder`, `Platform`, `SlotMapping`, `SourceRegistry`, `TestGraphBuilder`, `ObsidianMCPClient`, `temp_dir`, `SKU`, `BOQValidator`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `RepoManager` (e.g. with `LearningEngine` and `BaseEngineeringObject`) actually correct?**
  _`RepoManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `OKFReader` (e.g. with `BaseEngineeringObject` and `CategoryLimit`) actually correct?**
  _`OKFReader` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PDFExtractor` (e.g. with `TestIngestion` and `TestPlatformIdentityAgainstRealPDFs`) actually correct?**
  _`PDFExtractor` has 2 INFERRED edges - model-reasoned connections that need verification._