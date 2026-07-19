# Graph Report - vendorsolution_okf  (2026-07-20)

## Corpus Check
- 100 files · ~45,387 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 899 nodes · 2232 edges · 65 communities (48 shown, 17 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 393 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3bb256f5`
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
- Rule
- ._read_frontmatter
- mcp_server.py
- SourceWatcher
- SlotMapping

## God Nodes (most connected - your core abstractions)
1. `Platform` - 69 edges
2. `BaseEngineeringObject` - 62 edges
3. `HPEQuickSpecsAdapter` - 61 edges
4. `RepoManager` - 55 edges
5. `EvidenceRecord` - 51 edges
6. `Component` - 45 edges
7. `GraphBuilder` - 45 edges
8. `EngineeringRelationship` - 43 edges
9. `RuleEngine` - 43 edges
10. `Source` - 42 edges

## Surprising Connections (you probably didn't know these)
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFWriter` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (65 total, 17 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.11
Nodes (20): BaseEngineeringObject, Configuration, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R, SolutionCategory, Variant (+12 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 3 - "cli.py"
Cohesion: 0.05
Nodes (38): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+30 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.11
Nodes (19): Any, Run a user query through the end-to-end multi-step pipeline., Any, GraphBuilder, IntentParser, Deterministically validate the drafted BOM using the static RuleEngine., Dynamically recover from validation failures.         1. Try next candidate in r, Encapsulates the process nodes for the LangGraph state machine. (+11 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.14
Nodes (15): Intent Parser — Extracts structured engineering requirements from natural langua, GraphBuilder, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluates a set of component IDs against the canonical graph to ensure     all c, RuleEngine, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, # NOTE: `evidence` is NOT in the exclude set above, so it's already (+7 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (28): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+20 more)

### Community 9 - "IntentParser"
Cohesion: 0.05
Nodes (27): Client, ComponentSelectionResult, IntentParseResult, KeyManager, LLMClient, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and (+19 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.09
Nodes (21): DataFrame, ExcelExtractor, Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., PDFExtractor, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U (+13 more)

### Community 12 - "ConfidenceLevel"
Cohesion: 0.18
Nodes (6): Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.12
Nodes (11): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Load pending deltas from disk., Save a single delta to disk. (+3 more)

### Community 18 - "TestOKFWriter"
Cohesion: 0.18
Nodes (8): OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re, TestOKFWriter

### Community 19 - "graph.py"
Cohesion: 0.10
Nodes (14): DiGraph, GraphBuilder, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On). (+6 more)

### Community 20 - "RuleEngine"
Cohesion: 0.20
Nodes (5): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut

### Community 21 - "RepoManager"
Cohesion: 0.19
Nodes (18): BackgroundTasks, FastAPI, approve_delta(), approve_object(), get_integrations_status(), get_pending_deltas(), get_repo(), get_review_queue() (+10 more)

### Community 22 - "Platform"
Cohesion: 0.13
Nodes (6): Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does, Extract the main platform identity from the document using generalized heuristic

### Community 23 - "api.py"
Cohesion: 0.15
Nodes (12): CompiledStateGraph, GraphBuilder, build_workflow_graph(), GraphBuilder, IntentParser, Conditional edge router based on BOM validation with bounded retries., Conditional edge router after select_recovery_strategy., Conditional edge router for portal validation failures. (+4 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.10
Nodes (23): Extract memory specifications., Extract storage / drive cage specifications., Excel Source Parser — Extracts engineering objects from structured spreadsheets., CategoryLimit, Component, EngineeringRelationship, A directed, typed, evidence-backed relationship between two engineering objects., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl (+15 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.12
Nodes (36): datetime, Enum, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ConfidenceLevel, Constraint, EngineeringAttribute, EngineeringObjectType (+28 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.40
Nodes (4): IKP Platform State, Knowledge Graph Statistics, Objects by Type, Recent Architecture Changes

### Community 41 - "api.py"
Cohesion: 0.07
Nodes (30): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., Any, TableParser (+22 more)

### Community 50 - "Source"
Cohesion: 0.29
Nodes (13): ApprovalRequest, BOQValidationRequest, BaseModel, QueryRequest, SearchRequest, ValidationRequest, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, DeltaStatus (+5 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.15
Nodes (18): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, SKU, Workload, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_ (+10 more)

### Community 53 - "CustomerRequest"
Cohesion: 0.13
Nodes (28): CustomerRequest, CustomerRequirement, BaseModel, A single structured requirement extracted from a customer request., Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, ValidationFailure (+20 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.13
Nodes (10): Repository Manager — Orchestrates bidirectional sync between OKF files and the i, (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, Path, Background watcher that monitors the repository/ directory for external edits, RepositoryWatcher (+2 more)

### Community 62 - "._read_frontmatter"
Cohesion: 0.17
Nodes (7): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object., Return graph statistics for observability.

### Community 63 - "mcp_server.py"
Cohesion: 0.14
Nodes (12): IntentParser, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., call_tool(), get_repo(), list_tools(), List available tools., test_intent_parser() (+4 more)

### Community 64 - "SourceWatcher"
Cohesion: 0.43
Nodes (6): generate_tree(), main(), parse_python_ast(), parse_typescript_regex(), Extracts class and function signatures from a Python file using AST., Extracts classes and functions from TS/JS using basic regex to save tokens.

### Community 74 - "SlotMapping"
Cohesion: 0.09
Nodes (22): HPEQuickSpecsAdapter, Any, Extract power supply specifications., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects, Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende (+14 more)

## Knowledge Gaps
- **90 isolated node(s):** `Recent Architecture Changes`, `Knowledge Graph Statistics`, `Objects by Type`, `$schema`, `typescript` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseEngineeringObject` connect `OKFReader` to `GraphBuilder`, `api.py`, `SlotMapping`, `SolutionGenerator`, `ConfidenceLevel`, `IntentParser`, `BaseEngineeringObject`, `TestGraphBuilder`, `Source`, `test_graph_field_parity.py`, `graph.py`, `CustomerRequest`, `TestOKFWriter`, `RepositoryWatcher`, `ExcelExtractor`, `test_foundation.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepositoryWatcher` to `OKFReader`, `cli.py`, `SlotMapping`, `SolutionGenerator`, `ConfidenceLevel`, `BaseEngineeringObject`, `TestGraphBuilder`, `Source`, `TestOKFWriter`, `RepoManager`, `ExcelExtractor`, `test_foundation.py`, `mcp_server.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `HPEQuickSpecsAdapter` connect `SlotMapping` to `OKFReader`, `LLMClient`, `api.py`, `IntentParser`, `SolutionGenerator`, `test_graph_field_parity.py`, `Platform`, `ExcelExtractor`, `test_foundation.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `BaseEngineeringObject`) actually correct?**
  _`HPEQuickSpecsAdapter` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 17 INFERRED edges - model-reasoned connections that need verification._