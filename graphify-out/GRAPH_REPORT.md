# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 91 files · ~38,141 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 778 nodes · 2023 edges · 62 communities (50 shown, 12 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 384 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ef6a0b8b`
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

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 67 edges
2. `GraphBuilder` - 64 edges
3. `Platform` - 58 edges
4. `BaseEngineeringObject` - 55 edges
5. `RepoManager` - 54 edges
6. `EvidenceRecord` - 53 edges
7. `OKFReader` - 43 edges
8. `RuleEngine` - 42 edges
9. `EngineeringRelationship` - 41 edges
10. `Component` - 41 edges

## Surprising Connections (you probably didn't know these)
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestCategoryLimits` --uses--> `RelationshipType`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (62 total, 12 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.09
Nodes (22): Configuration, PackagingType, Packaging classification for components and SKUs., Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, SolutionCategory, Variant (+14 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.07
Nodes (52): ABC, DataFrame, FastAPI, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue() (+44 more)

### Community 2 - "IntentParser"
Cohesion: 0.13
Nodes (9): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+1 more)

### Community 3 - "RepoManager"
Cohesion: 0.18
Nodes (16): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+8 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "Component"
Cohesion: 0.15
Nodes (14): Any, [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop., [PLACEHOLDER] - Future Human-In-The-Loop (HITL) step., Traverse HasSKU edges and rank solutions based on business logic., Encapsulates the process nodes for the LangGraph state machine., Parse the unstructured customer message into strict requirements., Select a platform that Supports the chosen workload. (+6 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.08
Nodes (17): Any, GraphBuilder, Any, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria. (+9 more)

### Community 7 - "App.tsx"
Cohesion: 0.09
Nodes (20): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+12 more)

### Community 8 - "models.py"
Cohesion: 0.15
Nodes (19): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluates a set of component IDs against the canonical graph to ensure     all c, RuleEngine, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent. (+11 more)

### Community 9 - "cli.py"
Cohesion: 0.32
Nodes (6): call_tool(), get_repo(), list_tools(), List available tools., TextContent, Tool

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.19
Nodes (9): Minimum relationship types from Blueprint 03 §7., RelationshipType, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already, api_client(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje (+1 more)

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
Cohesion: 0.33
Nodes (3): Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract engineering rules from notes, warnings, and constraints.

### Community 16 - "Platform"
Cohesion: 0.14
Nodes (8): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu

### Community 17 - "TestGraphBuilder"
Cohesion: 0.11
Nodes (18): Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, Create a small test graph with known structure., TestGraphBuilder, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_ (+10 more)

### Community 18 - "SourceRegistry"
Cohesion: 0.06
Nodes (69): datetime, Enum, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parses Excel spreadsheets into IKP canonical objects., PDFExtractor, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Extract product description from introductory text. (+61 more)

### Community 19 - "Platform"
Cohesion: 0.14
Nodes (8): OKFWriter, Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Writes engineering knowledge to disk in OKF format., Read YAML frontmatter from an OKF Markdown file., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.19
Nodes (5): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis, Repository Manager — Orchestrates bidirectional sync between OKF files and the i

### Community 21 - "LearningEngine"
Cohesion: 0.12
Nodes (12): (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, Load all existing OKF files into the in-memory graph.         Returns the number (+4 more)

### Community 22 - "SKU"
Cohesion: 0.27
Nodes (6): Extract memory specifications., CategoryLimit, Component, A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category, TestCategoryLimits

### Community 23 - "BOQValidator"
Cohesion: 0.24
Nodes (5): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, TestFuzzyMatching

### Community 24 - "Component"
Cohesion: 0.10
Nodes (15): Stage 1: Normalize invisible PDF typography and Unicode artifacts., Extract spatial topology and slot mappings., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract storage / drive cage specifications., Extract networking/OCP/NIC information., Extract GPU/accelerator information. (+7 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - ".filter_by_metadata"
Cohesion: 0.21
Nodes (7): Path, Attempt to infer vendor from filename., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., Compute SHA-256 hash of a file for duplicate detection., SourceRegistry

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 49 - "SlotMapping"
Cohesion: 0.18
Nodes (10): EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, temp_repo(), Regression test for the direction-assumption bug found alongside the     field-p, test_compatibility_check_finds_reverse_direction_contains_edge(), Test that relationships (edges) and body contents survive a restart/roundtrip., test_okf_persistence_roundtrip() (+2 more)

### Community 50 - "BaseEngineeringObject"
Cohesion: 0.29
Nodes (6): BaseEngineeringObject, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Add a concept and all its attributes as a node in the graph.          Field mapp, Vectorize and index a single object. Prefer index_many() for         bulk ingest, Vectorize and index a list of objects, batching embedding API         calls in g, VectorStore

### Community 51 - "._compute_path"
Cohesion: 0.29
Nodes (4): Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug.

### Community 52 - "SourceWatcher"
Cohesion: 0.29
Nodes (4): Source Watcher — Detects new engineering sources in the sources/ directory.  Gov, Monitors the sources/ directory tree for new or changed files.     Maintains a s, Scan the sources directory for new files.         Returns list of absolute paths, SourceWatcher

### Community 53 - "build_workflow_graph"
Cohesion: 0.29
Nodes (7): build_workflow_graph(), Conditional edge router based on BOM validation., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine., should_human_intervene(), should_loop_bom(), StateGraph

### Community 54 - "shared_temp_dir"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

### Community 55 - "temp_dir"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

### Community 56 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

## Knowledge Gaps
- **87 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+82 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `Component`, `models.py`, `PDFExtractor`, `TestGraphBuilder`, `BaseEngineeringObject`, `SourceRegistry`, `ObsidianMCPClient`, `LearningEngine`, `build_workflow_graph`, `BOQValidator`, `SKU`, `SlotMapping`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `PDFExtractor` connect `SourceRegistry` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `RepoManager`, `PDFExtractor`, `._extract_platform_identity`, `SlotMapping`, `BaseEngineeringObject`, `TestGraphBuilder`, `BOQValidator`, `ObsidianMCPClient`, `SKU`, `temp_dir`, `._process_structured_components`, `Component`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `LearningEngine` to `BaseEngineeringObject`, `EvidenceRecord`, `RepoManager`, `GraphBuilder`, `cli.py`, `PDFExtractor`, `Platform`, `SlotMapping`, `SourceRegistry`, `BaseEngineeringObject`, `ObsidianMCPClient`, `Platform`, `TestGraphBuilder`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Platform` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`Platform` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 13 INFERRED edges - model-reasoned connections that need verification._