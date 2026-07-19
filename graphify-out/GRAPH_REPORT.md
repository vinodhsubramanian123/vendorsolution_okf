# Graph Report - vendorsolution_okf  (2026-07-20)

## Corpus Check
- 100 files · ~45,352 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 890 nodes · 2306 edges · 68 communities (56 shown, 12 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 430 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `41ef1f83`
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
- llm_client.py
- ._read_frontmatter
- mcp_server.py
- SourceWatcher
- TestPlatformIdentityAgainstRealPDFs
- ._process_structured_components
- SlotMapping

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

## Communities (68 total, 12 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.12
Nodes (13): OKFReader, Any, Path, Helper to build a Pydantic object from frontmatter and body., Split an OKF file into (frontmatter_dict, body_str)., Extract relationships from the Markdown body's Relationships section., Extract evidence from the Citations section (OKF §8)., Extract text content under a specific heading. (+5 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.16
Nodes (9): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, PackagingType, Packaging classification for components and SKUs., An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, Blueprint 03 §8: Rule must expose scope, confidence, evidence, version., Direct regression test for the specific dedup bug found in the     2026-07-18 au, test_platform_id_survives_for_rule_dedup() (+1 more)

### Community 3 - "cli.py"
Cohesion: 0.06
Nodes (33): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+25 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.12
Nodes (17): Any, Run a user query through the end-to-end multi-step pipeline., Any, Deterministically validate the drafted BOM using the static RuleEngine., Dynamically recover from validation failures.         1. Try next candidate in r, Encapsulates the process nodes for the LangGraph state machine., [PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals., [PLACEHOLDER] - Future Knowledge Update Loop. (+9 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.10
Nodes (18): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, GraphBuilder, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri (+10 more)

### Community 7 - "App.tsx"
Cohesion: 0.08
Nodes (28): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+20 more)

### Community 8 - "EvidenceRecord"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 9 - "IntentParser"
Cohesion: 0.06
Nodes (25): Client, ComponentSelectionResult, IntentParseResult, KeyManager, LLMClient, Any, BaseModel, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and (+17 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.15
Nodes (15): PDFExtractor, Any, Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.     U, Normalize typography and whitespace., Fallback when automated extraction fails or no adapter is found.         Dumps f, TableParser, Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source (+7 more)

### Community 12 - "ConfidenceLevel"
Cohesion: 0.29
Nodes (4): Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Load all existing OKF files into the in-memory graph.         Returns the number, Add a new engineering concept to both layers.         Returns the relative path

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 15 - "Component"
Cohesion: 0.20
Nodes (9): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir() (+1 more)

### Community 16 - "BaseEngineeringObject"
Cohesion: 0.11
Nodes (12): LearningEngine, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Load pending deltas from disk. (+4 more)

### Community 17 - "TestGraphBuilder"
Cohesion: 0.22
Nodes (4): Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, Create a small test graph with known structure., TestGraphBuilder

### Community 18 - "TestOKFWriter"
Cohesion: 0.18
Nodes (8): OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug., Generate OKF-compliant YAML frontmatter with full metadata.          OKF §4.1 Re, TestOKFWriter

### Community 20 - "RuleEngine"
Cohesion: 0.20
Nodes (9): ValidationFailure, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates a set of component IDs against the canonical graph to ensure     all c, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine (+1 more)

### Community 21 - "RepoManager"
Cohesion: 0.22
Nodes (16): BackgroundTasks, approve_delta(), approve_object(), get_integrations_status(), get_pending_deltas(), get_repo(), get_review_queue(), get_status() (+8 more)

### Community 22 - "Platform"
Cohesion: 0.10
Nodes (12): HPEQuickSpecsAdapter, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags. (+4 more)

### Community 23 - "api.py"
Cohesion: 0.20
Nodes (9): CompiledStateGraph, build_workflow_graph(), Conditional edge router based on BOM validation with bounded retries., Conditional edge router after select_recovery_strategy., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine., route_recovery(), should_human_intervene() (+1 more)

### Community 24 - "ExcelExtractor"
Cohesion: 0.10
Nodes (20): Extract power supply specifications., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract memory specifications., Extract storage / drive cage specifications., Extract networking/OCP/NIC information., Extract GPU/accelerator information. (+12 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.13
Nodes (34): Enum, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parses Excel spreadsheets into IKP canonical objects., Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ConfidenceLevel, DeltaChangeType, DeltaStatus (+26 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "api.py"
Cohesion: 0.17
Nodes (9): BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, BaseModel, A single message from a validation check., Complete result of validating a solution candidate.     Blueprint 06 §9: Portal, ValidationMessage, ValidationResult (+1 more)

### Community 50 - "Source"
Cohesion: 0.15
Nodes (12): KnowledgeDelta, Every newly acquired engineering source produces a Knowledge Delta.     Blueprin, Apply a validated Knowledge Delta — persist all objects and record the delta., Record a Knowledge Delta in the history/ directory., ManualReviewValidator, ABC, Vendor Validation — Abstract interface for vendor validation integration.  Gover, V1.0 implementation: flags solutions for human engineering review.     Blueprint (+4 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.15
Nodes (18): Component, EngineeringAttribute, A typed, structured engineering attribute., A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_ (+10 more)

### Community 52 - "Platform"
Cohesion: 0.18
Nodes (9): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., DeltaChange, A single change within a Knowledge Delta. (+1 more)

### Community 53 - "CustomerRequest"
Cohesion: 0.14
Nodes (33): mock_evaluate(), ApprovalRequest, BOQValidationRequest, BaseModel, QueryRequest, SearchRequest, ValidationRequest, CustomerRequest (+25 more)

### Community 54 - "RepositoryWatcher"
Cohesion: 0.10
Nodes (13): FastAPI, lifespan(), (Re)build the semantic search index from everything currently on         disk in, Update CONTEXT.md with current engineering coverage., Central orchestrator for the dual-layer architecture.      - Persistence layer:, RepoManager, Path, Background watcher that monitors the repository/ directory for external edits (+5 more)

### Community 55 - "ExcelExtractor"
Cohesion: 0.27
Nodes (7): DataFrame, Parse a dataframe of components., Parse a dataframe of SKUs., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., EvidenceRecord, BaseModel, Tracks provenance of an engineering fact.     Blueprint 06 §7: "Never overwrite

### Community 56 - "Rule"
Cohesion: 0.15
Nodes (19): datetime, BaseEngineeringObject, Configuration, Constraint, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL (+11 more)

### Community 57 - "llm_client.py"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

### Community 62 - "._read_frontmatter"
Cohesion: 0.17
Nodes (7): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object., Return graph statistics for observability.

### Community 63 - "mcp_server.py"
Cohesion: 0.16
Nodes (10): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., call_tool(), get_repo(), test_intent_parser(), test_rule_engine() (+2 more)

### Community 64 - "SourceWatcher"
Cohesion: 0.43
Nodes (6): generate_tree(), main(), parse_python_ast(), parse_typescript_regex(), Extracts class and function signatures from a Python file using AST., Extracts classes and functions from TS/JS using basic regex to save tokens.

### Community 73 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

### Community 74 - "SlotMapping"
Cohesion: 0.38
Nodes (4): Extract spatial topology and slot mappings., Spatial topology mapping for physical components., SlotMapping, TestTopology

## Knowledge Gaps
- **89 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `WorkflowNodes`, `IntentParser`, `api.py`, `SolutionGenerator`, `Component`, `TestGraphBuilder`, `TestOKFWriter`, `graph.py`, `RuleEngine`, `CustomerRequest`, `RepositoryWatcher`, `api.py`, `Rule`, `ExcelExtractor`, `test_graph_field_parity.py`, `test_foundation.py`, `._read_frontmatter`, `mcp_server.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepositoryWatcher` to `OKFReader`, `cli.py`, `GraphBuilder`, `IntentParser`, `SolutionGenerator`, `ConfidenceLevel`, `Component`, `BaseEngineeringObject`, `TestGraphBuilder`, `Source`, `TestOKFWriter`, `CustomerRequest`, `RepoManager`, `ExcelExtractor`, `Rule`, `test_foundation.py`, `mcp_server.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `Rule` to `OKFReader`, `LLMClient`, `GraphBuilder`, `IntentParser`, `SolutionGenerator`, `ConfidenceLevel`, `BaseEngineeringObject`, `TestGraphBuilder`, `TestOKFWriter`, `Platform`, `ExcelExtractor`, `test_foundation.py`, `Source`, `test_graph_field_parity.py`, `Platform`, `RepositoryWatcher`, `ExcelExtractor`, `._process_structured_components`, `SlotMapping`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `BaseEngineeringObject`) actually correct?**
  _`HPEQuickSpecsAdapter` has 27 INFERRED edges - model-reasoned connections that need verification._