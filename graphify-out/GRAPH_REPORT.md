# Graph Report - vendorsolution_okf  (2026-07-18)

## Corpus Check
- 79 files · ~52,135 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 703 nodes · 1508 edges · 61 communities (52 shown, 9 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 271 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fcd73cc6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- IKP Platform State
- Vendorsolution OKF
- Cross-Platform Toolchain Setup
- agy
- pip
- python
- api.py
- PDFExtractor
- RepoManager
- LLMClient
- App.tsx
- BaseModel
- ._read_frontmatter
- Source
- TableParser
- Coverage
- IKP Operations Log
- conftest.py
- TestIngestion
- GraphBuilder
- compilerOptions
- compilerOptions
- BaseEngineeringObject
- TestGraphBuilder
- RuleEngine
- RepoManager
- .add_concept
- RelationshipType
- SKU
- ObsidianMCPClient
- SourceWatcher
- logger.py
- SlotMapping
- test_mcp_integration.py
- test_api_endpoints.py
- tsconfig.json
- bootstrap.sh
- .filter_by_metadata
- pdf_extractor.py
- mcp_server.py
- TestPlatformIdentityAgainstRealPDFs
- ._process_structured_components
- ._build_candidate
- .apply_delta
- .get_dependencies
- .test_source_registration
- ._extract_rules
- temp_dir
- BaseModel

## God Nodes (most connected - your core abstractions)
1. `GraphBuilder` - 50 edges
2. `RepoManager` - 47 edges
3. `PDFExtractor` - 43 edges
4. `TestGraphBuilder` - 41 edges
5. `TestOntologyModels` - 34 edges
6. `TestOKFWriter` - 34 edges
7. `Platform` - 33 edges
8. `BaseEngineeringObject` - 31 edges
9. `Source` - 31 edges
10. `TestOKFReader` - 30 edges

## Surprising Connections (you probably didn't know these)
- `TestIngestion` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestCategoryLimits` --uses--> `GraphBuilder`  [INFERRED]
  tests/test_category_limits.py → ikp_platform/core/repository/graph_builder.py
- `TestGraphBuilder` --uses--> `GraphBuilder`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/repository/graph_builder.py
- `TestOKFReader` --uses--> `GraphBuilder`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/repository/graph_builder.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (61 total, 9 thin omitted)

### Community 0 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 1 - "Vendorsolution OKF"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 2 - "Cross-Platform Toolchain Setup"
Cohesion: 0.14
Nodes (12): OKFReader, Any, BaseEngineeringObject, Path, Helper to build a Pydantic object from frontmatter and body., Split an OKF file into (frontmatter_dict, body_str)., Extract text content under a specific heading., Extract a bulleted list under a specific heading. (+4 more)

### Community 6 - "api.py"
Cohesion: 0.13
Nodes (26): ABC, Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, DeltaChange, DeltaChangeType, EvidenceRecord, HistoryEntry, KnowledgeDelta, BaseModel (+18 more)

### Community 7 - "PDFExtractor"
Cohesion: 0.21
Nodes (7): PDFExtractor, Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Extract the main platform identity from the document using generalized heuristic, Extracts engineering knowledge from vendor QuickSpecs and technical PDFs.      B

### Community 8 - "RepoManager"
Cohesion: 0.06
Nodes (33): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+25 more)

### Community 9 - "LLMClient"
Cohesion: 0.14
Nodes (9): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+1 more)

### Community 10 - "App.tsx"
Cohesion: 0.09
Nodes (16): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, SemanticSearch(), Sidebar(), SidebarProps (+8 more)

### Community 11 - "BaseModel"
Cohesion: 0.18
Nodes (11): Component, EngineeringRelationship, EvidenceRecord, Extract processor specifications from QuickSpecs tables., Extract networking/OCP/NIC information., Extract GPU/accelerator information., Extract power supply specifications., Extract relationships from the Markdown body's Relationships section. (+3 more)

### Community 12 - "._read_frontmatter"
Cohesion: 0.14
Nodes (13): OKFWriter, Any, BaseEngineeringObject, Path, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Generate an index.md for the given directory listing all .md concepts.         O (+5 more)

### Community 13 - "Source"
Cohesion: 0.06
Nodes (33): axios, dependencies, axios, lucide-react, react, react-dom, devDependencies, oxlint (+25 more)

### Community 14 - "TableParser"
Cohesion: 0.16
Nodes (13): DataFrame, ExcelExtractor, Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., CategoryLimit, Component (+5 more)

### Community 15 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 16 - "IKP Operations Log"
Cohesion: 0.33
Nodes (5): 2026-07-15, 2026-07-16, 2026-07-17, 2026-07-18, IKP Operations Log

### Community 17 - "conftest.py"
Cohesion: 0.08
Nodes (31): BaseModel, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status(), query_solution() (+23 more)

### Community 18 - "TestIngestion"
Cohesion: 0.13
Nodes (34): datetime, Enum, Excel Source Parser — Extracts engineering objects from structured spreadsheets., Source Registry — Registers, classifies, and tracks engineering sources.  Govern, ConfidenceLevel, CustomerRequirement, DeltaStatus, EngineeringObjectType (+26 more)

### Community 19 - "GraphBuilder"
Cohesion: 0.26
Nodes (7): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluates a set of component IDs against the canonical graph to ensure     all c, RuleEngine, Any, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, main(), main()

### Community 20 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 21 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 23 - "TestGraphBuilder"
Cohesion: 0.20
Nodes (6): EngineeringAttribute, A typed, structured engineering attribute., Customer intent rather than products.     Blueprint 03 §11: Workloads SHALL neve, Workload, Create a small test graph with known structure., TestGraphBuilder

### Community 24 - "RuleEngine"
Cohesion: 0.20
Nodes (5): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut

### Community 25 - "RepoManager"
Cohesion: 0.36
Nodes (3): Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., TestOKFWriter

### Community 26 - ".add_concept"
Cohesion: 0.14
Nodes (8): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu

### Community 27 - "RelationshipType"
Cohesion: 0.23
Nodes (6): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., test_intent_parser(), test_solution_generator()

### Community 28 - "SKU"
Cohesion: 0.24
Nodes (5): Any, Vectorize and index a single object. Prefer index_many() for         bulk ingest, Vectorize and index a list of objects, batching embedding API         calls in g, Search the vector database and return a list of matching IDs., VectorStore

### Community 29 - "ObsidianMCPClient"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis

### Community 30 - "SourceWatcher"
Cohesion: 0.19
Nodes (6): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, TestFuzzyMatching

### Community 31 - "logger.py"
Cohesion: 0.24
Nodes (6): BaseEngineeringObject, KnowledgeDelta, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Extract memory specifications., Extract storage / drive cage specifications., Main extraction entry point.         Returns (list of engineering objects, knowl

### Community 32 - "SlotMapping"
Cohesion: 0.60
Nodes (3): Spatial topology mapping for physical components., SlotMapping, TestTopology

### Community 33 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 47 - ".filter_by_metadata"
Cohesion: 0.25
Nodes (5): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all objects compatible with the given object.

### Community 48 - "pdf_extractor.py"
Cohesion: 0.09
Nodes (16): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser, An engineering rule with full metadata.     Blueprint 03 §8: Every rule SHALL ex, Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Rule, Source (+8 more)

### Community 49 - "mcp_server.py"
Cohesion: 0.33
Nodes (5): call_tool(), list_tools(), List available tools., TextContent, Tool

### Community 50 - "TestPlatformIdentityAgainstRealPDFs"
Cohesion: 0.20
Nodes (6): Extract spatial topology and slot mappings., Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Fallback when automated title/vendor/domain extraction fails.          This does, Extract high-level Workloads (Customer Intent) and link to Platform., Platform, Workload

### Community 51 - "._process_structured_components"
Cohesion: 0.40
Nodes (3): Any, Classify a component description into (category, subcategory) using keyword scor, Convert structured dictionary rows from TableParser into Component + SKU objects

### Community 52 - "._build_candidate"
Cohesion: 0.22
Nodes (10): CustomerRequest, Structured customer engineering request.     Blueprint 05 §4: Customer requests, A generated solution with full explainability.     Blueprint 05 §13: Every recom, SolutionCandidate, Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, Builds a single candidate and validates it., Generates explainable solution candidates based on customer intent., Generate multiple solution profiles.         Blueprint 05 §13: Where appropriate (+2 more)

### Community 53 - ".apply_delta"
Cohesion: 0.20
Nodes (10): BaseEngineeringObject, Configuration, Constraint, The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng, An engineering limitation (max controllers, max drives, max memory, etc.).     B, Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tow, A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')., A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN R (+2 more)

### Community 54 - ".get_dependencies"
Cohesion: 0.10
Nodes (11): GraphBuilder, BaseEngineeringObject, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri, Find all simple paths between two engineering concepts., Get all outbound dependency targets (Requires, Depends On). (+3 more)

### Community 55 - ".test_source_registration"
Cohesion: 0.25
Nodes (7): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir()

### Community 56 - "._extract_rules"
Cohesion: 0.29
Nodes (4): Returns True if the rule contains negation phrasing that should reverse/discard, Strips leading conditionals like 'If X, then Y' down to just 'Y' for the depende, Extract engineering rules from notes, warnings, and constraints., Rule

## Knowledge Gaps
- **85 isolated node(s):** `Solution Domains`, `Sources Ingested: 1`, `Learnings & Architecture Updates (Agent Run)`, `2026-07-18`, `2026-07-17` (+80 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `PDFExtractor` to `RepoManager`, `LLMClient`, `BaseModel`, `pdf_extractor.py`, `TestPlatformIdentityAgainstRealPDFs`, `._process_structured_components`, `GraphBuilder`, `BaseEngineeringObject`, `._extract_rules`, `logger.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `conftest.py` to `Cross-Platform Toolchain Setup`, `api.py`, `RepoManager`, `BaseModel`, `._read_frontmatter`, `pdf_extractor.py`, `mcp_server.py`, `TestIngestion`, `TestGraphBuilder`, `.get_dependencies`, `.test_source_registration`, `RepoManager`, `.add_concept`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `.get_dependencies` to `Cross-Platform Toolchain Setup`, `TableParser`, `.filter_by_metadata`, `conftest.py`, `TestIngestion`, `GraphBuilder`, `._build_candidate`, `TestGraphBuilder`, `.test_source_registration`, `RepoManager`, `RelationshipType`, `SourceWatcher`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `PDFExtractor` (e.g. with `LLMClient` and `TestIngestion`) actually correct?**
  _`PDFExtractor` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `TestGraphBuilder` (e.g. with `BaseEngineeringObject` and `Component`) actually correct?**
  _`TestGraphBuilder` has 28 INFERRED edges - model-reasoned connections that need verification._