# Graph Report - vendorsolution_okf  (2026-07-19)

## Corpus Check
- 93 files · ~40,599 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 811 nodes · 2089 edges · 49 communities (40 shown, 9 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 393 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dd13cc31`
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
- IntentParser
- compilerOptions
- SolutionGenerator
- compilerOptions
- Setup
- TestGraphBuilder
- TestOKFWriter
- RepoManager
- Platform
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
- CustomerRequest
- .traverse_relationships
- models.py

## God Nodes (most connected - your core abstractions)
1. `Platform` - 65 edges
2. `HPEQuickSpecsAdapter` - 64 edges
3. `GraphBuilder` - 64 edges
4. `BaseEngineeringObject` - 63 edges
5. `RepoManager` - 54 edges
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

## Communities (49 total, 9 thin omitted)

### Community 0 - "OKFReader"
Cohesion: 0.12
Nodes (13): OKFReader, Any, Path, Helper to build a Pydantic object from frontmatter and body., Split an OKF file into (frontmatter_dict, body_str)., Extract relationships from the Markdown body's Relationships section., Extract evidence from the Citations section (OKF §8)., Parses OKF Markdown files and reconstructs Pydantic engineering objects. (+5 more)

### Community 1 - "TableParser"
Cohesion: 0.33
Nodes (3): Any, Parses PDF tables using pdfplumber to accurately extract SKUs,     bracketed not, TableParser

### Community 2 - "LLMClient"
Cohesion: 0.09
Nodes (14): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+6 more)

### Community 3 - "cli.py"
Cohesion: 0.06
Nodes (33): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+25 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (38): axios, dependencies, axios, lucide-react, react, react-dom, react-markdown, devDependencies (+30 more)

### Community 5 - "WorkflowNodes"
Cohesion: 0.11
Nodes (21): build_workflow_graph(), Conditional edge router based on BOM validation with bounded retries., Conditional edge router for portal validation failures., Builds and wires the LangGraph StateMachine., should_human_intervene(), should_loop_bom(), Any, Deterministically validate the drafted BOM using the static RuleEngine. (+13 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.07
Nodes (21): DiGraph, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Evaluates a set of component IDs against the canonical graph to ensure     all c, Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine (+13 more)

### Community 7 - "App.tsx"
Cohesion: 0.09
Nodes (20): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), KnowledgeTransfer(), PlatformDashboard() (+12 more)

### Community 9 - "IntentParser"
Cohesion: 0.18
Nodes (11): CustomerRequirement, A single structured requirement extracted from a customer request., IntentParser, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., call_tool(), get_repo(), list_tools() (+3 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "SolutionGenerator"
Cohesion: 0.15
Nodes (15): Decorator for end-to-end observability.     Logs method entry, exit, duration, e, telemetry_trace(), Intent Parser — Extracts structured engineering requirements from natural langua, Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Generates explainable solution candidates based on customer intent., SolutionGenerator, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov (+7 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (15): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Architecture & Capabilities, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install (+7 more)

### Community 17 - "TestGraphBuilder"
Cohesion: 0.22
Nodes (4): Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, Create a small test graph with known structure., TestGraphBuilder

### Community 18 - "TestOKFWriter"
Cohesion: 0.11
Nodes (16): An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Rule, OKFWriter, Any, Path, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Generate an index.md for the given directory listing all .md concepts.         O (+8 more)

### Community 21 - "RepoManager"
Cohesion: 0.05
Nodes (29): Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, ObsidianMCPClient, Synchronous wrapper to execute a search against the vault.         Returns a lis, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Repository Manager — Orchestrates bidirectional sync between OKF files and the i, (Re)build the semantic search index from everything currently on         disk in, Apply a validated Knowledge Delta — persist all objects and record the delta. (+21 more)

### Community 22 - "Platform"
Cohesion: 0.05
Nodes (46): BasePDFAdapter, ABC, Returns True if this adapter can process the given PDF text., Extract the main platform object from the text., Extract all related components, rules, and workloads from the text and tables., Base class for vendor-specific PDF extraction logic., HPEQuickSpecsAdapter, Any (+38 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - "test_foundation.py"
Cohesion: 0.18
Nodes (25): Enum, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, DeltaStatus, EngineeringAttribute, EngineeringObjectType, LifecycleStatus, PackagingType, ProcessingStatus (+17 more)

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 41 - "api.py"
Cohesion: 0.08
Nodes (50): FastAPI, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status(), lifespan() (+42 more)

### Community 50 - "Source"
Cohesion: 0.07
Nodes (29): DataFrame, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., PDFExtractor (+21 more)

### Community 51 - "test_graph_field_parity.py"
Cohesion: 0.12
Nodes (17): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, TestFuzzyMatching, _assert_every_field_reachable(), Regression guard for the "GraphBuilder silently drops a field" bug class.  Histo, Covers the exact fields ADR-001 fixed, plus every other Rule field., Covers the exact fields commit a6ef5df fixed (target_subcategory,     component_, Workload requirements are flattened rather than kept as nested dicts     -- conf (+9 more)

### Community 53 - "CustomerRequest"
Cohesion: 0.13
Nodes (16): CustomerRequest, HistoryEntry, BaseModel, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, Builds a single candidate and validates it. (+8 more)

### Community 54 - ".traverse_relationships"
Cohesion: 0.20
Nodes (6): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all related node IDs traversing both inbound and outbound edges.          Th, Get all objects compatible with the given object.

### Community 58 - "models.py"
Cohesion: 0.15
Nodes (19): datetime, BaseEngineeringObject, Configuration, Constraint, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()., The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, Spatial topology mapping for physical components. (+11 more)

## Knowledge Gaps
- **88 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBuilder` connect `GraphBuilder` to `WorkflowNodes`, `api.py`, `SolutionGenerator`, `TestGraphBuilder`, `Source`, `TestOKFWriter`, `test_graph_field_parity.py`, `RepoManager`, `.traverse_relationships`, `CustomerRequest`, `Platform`, `models.py`, `test_foundation.py`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `BaseEngineeringObject` connect `models.py` to `OKFReader`, `LLMClient`, `GraphBuilder`, `api.py`, `SolutionGenerator`, `TestGraphBuilder`, `Source`, `TestOKFWriter`, `test_graph_field_parity.py`, `RepoManager`, `Platform`, `CustomerRequest`, `test_foundation.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `HPEQuickSpecsAdapter` connect `Platform` to `TableParser`, `LLMClient`, `api.py`, `TestGraphBuilder`, `TestOKFWriter`, `test_graph_field_parity.py`, `Source`, `RepoManager`, `models.py`, `test_foundation.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Platform` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`Platform` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `HPEQuickSpecsAdapter` (e.g. with `BasePDFAdapter` and `TableParser`) actually correct?**
  _`HPEQuickSpecsAdapter` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `BaseEngineeringObject` (e.g. with `BasePDFAdapter` and `HPEQuickSpecsAdapter`) actually correct?**
  _`BaseEngineeringObject` has 16 INFERRED edges - model-reasoned connections that need verification._