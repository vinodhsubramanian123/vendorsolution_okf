# Graph Report - vendorsolution_okf  (2026-07-18)

## Corpus Check
- 81 files · ~34,087 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 695 nodes · 1668 edges · 45 communities (34 shown, 11 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 298 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `01eb391f`
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
- ObsidianMCPClient
- SKU
- Coverage
- test_mcp_integration.py
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
- BaseModel

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 67 edges
2. `Platform` - 53 edges
3. `BaseEngineeringObject` - 50 edges
4. `GraphBuilder` - 49 edges
5. `RepoManager` - 46 edges
6. `EvidenceRecord` - 44 edges
7. `OKFReader` - 42 edges
8. `TestGraphBuilder` - 41 edges
9. `Source` - 37 edges
10. `Component` - 36 edges

## Surprising Connections (you probably didn't know these)
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestCategoryLimits` --uses--> `RelationshipType`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `RelationshipType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestExcelIngestion` --uses--> `SourceType`  [INFERRED]
  tests/test_excel_parser.py → ikp_platform/core/ontology/models.py
- `TestGraphBuilder` --uses--> `SourceType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (45 total, 11 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.05
Nodes (87): datetime, Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, BaseEngineeringObject, ConfidenceLevel, Configuration, Constraint (+79 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.08
Nodes (24): ABC, LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m (+16 more)

### Community 2 - "IntentParser"
Cohesion: 0.12
Nodes (10): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+2 more)

### Community 3 - "RepoManager"
Cohesion: 0.05
Nodes (39): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+31 more)

### Community 4 - "devDependencies"
Cohesion: 0.06
Nodes (33): axios, dependencies, axios, lucide-react, react, react-dom, devDependencies, oxlint (+25 more)

### Community 5 - "Component"
Cohesion: 0.06
Nodes (44): DataFrame, ExcelExtractor, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., Any (+36 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.08
Nodes (16): GraphBuilder, Any, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr (+8 more)

### Community 7 - "App.tsx"
Cohesion: 0.10
Nodes (19): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), PlatformDashboard(), SemanticSearch() (+11 more)

### Community 8 - "models.py"
Cohesion: 0.12
Nodes (10): BaseEngineeringObject, ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis, Any, Vectorize and index a single object. Prefer index_many() for         bulk ingest, Vectorize and index a list of objects, batching embedding API         calls in g (+2 more)

### Community 9 - "cli.py"
Cohesion: 0.17
Nodes (11): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., Generates explainable solution candidates based on customer intent., SolutionGenerator, call_tool(), test_intent_parser() (+3 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

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
Cohesion: 0.06
Nodes (25): PDFExtractor, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Classify a component description into (category, subcategory) using keyword scor, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract product description from introductory text., Extract chassis type variants. (+17 more)

### Community 16 - "Platform"
Cohesion: 0.67
Nodes (3): list_tools(), List available tools., Tool

### Community 18 - "SourceRegistry"
Cohesion: 0.21
Nodes (7): Path, Attempt to infer vendor from filename., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., Compute SHA-256 hash of a file for duplicate detection., SourceRegistry

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.27
Nodes (7): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluates a set of component IDs against the canonical graph to ensure     all c, RuleEngine, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, main(), main()

### Community 22 - "SKU"
Cohesion: 0.10
Nodes (25): BaseModel, GraphBuilder, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status() (+17 more)

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

## Knowledge Gaps
- **84 isolated node(s):** `Knowledge Graph Statistics`, `Objects by Type`, `2026-07-18`, `start_api.sh script`, `start_ui.sh script` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `._extract_platform_identity` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `RepoManager`, `Component`, `models.py`, `ObsidianMCPClient`, `SKU`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `GraphBuilder` to `BaseEngineeringObject`, `IntentParser`, `RepoManager`, `Component`, `models.py`, `cli.py`, `TestGraphBuilder`, `ObsidianMCPClient`, `SKU`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepoManager` to `BaseEngineeringObject`, `EvidenceRecord`, `Component`, `GraphBuilder`, `models.py`, `cli.py`, `._extract_platform_identity`, `TestGraphBuilder`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Platform` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`Platform` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 12 INFERRED edges - model-reasoned connections that need verification._