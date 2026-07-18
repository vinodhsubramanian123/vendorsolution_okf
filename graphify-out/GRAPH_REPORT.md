# Graph Report - vendorsolution_okf  (2026-07-18)

## Corpus Check
- 81 files · ~33,901 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 689 nodes · 1765 edges · 49 communities (37 shown, 12 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 365 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2310b0b7`
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
- conftest.py
- ObsidianMCPClient
- pdf_extractor.py
- SKU
- logger.py
- TestPlatformIdentityAgainstRealPDFs
- Coverage
- test_mcp_integration.py
- ._extract_rules
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

## God Nodes (most connected - your core abstractions)
1. `PDFExtractor` - 67 edges
2. `BaseEngineeringObject` - 55 edges
3. `Platform` - 53 edges
4. `RepoManager` - 53 edges
5. `GraphBuilder` - 52 edges
6. `EvidenceRecord` - 51 edges
7. `OKFReader` - 42 edges
8. `TestGraphBuilder` - 41 edges
9. `KnowledgeDelta` - 38 edges
10. `Source` - 37 edges

## Surprising Connections (you probably didn't know these)
- `TestExcelIngestion` --uses--> `ExcelExtractor`  [INFERRED]
  tests/test_excel_parser.py → ikp_platform/core/ingestion/excel_parser.py
- `TestIngestion` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestPlatformIdentityAgainstRealPDFs` --uses--> `PDFExtractor`  [INFERRED]
  tests/test_ingestion.py → ikp_platform/core/ingestion/pdf_extractor.py
- `TestGraphBuilder` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py
- `TestOKFReader` --uses--> `EngineeringObjectType`  [INFERRED]
  tests/test_foundation.py → ikp_platform/core/ontology/models.py

## Import Cycles
- 1-file cycle: `ikp_platform/mcp_server.py -> ikp_platform/mcp_server.py`

## Communities (49 total, 12 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.05
Nodes (59): BaseEngineeringObject, Configuration, Constraint, DeltaStatus, EngineeringAttribute, LifecycleStatus, Product lifecycle status for engineering objects., Knowledge Delta lifecycle status. (+51 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.08
Nodes (63): ABC, DataFrame, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status() (+55 more)

### Community 2 - "IntentParser"
Cohesion: 0.06
Nodes (26): CustomerRequirement, A single structured requirement extracted from a customer request., IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., LLMClient, Any (+18 more)

### Community 3 - "RepoManager"
Cohesion: 0.06
Nodes (21): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu (+13 more)

### Community 4 - "devDependencies"
Cohesion: 0.06
Nodes (33): axios, dependencies, axios, lucide-react, react, react-dom, devDependencies, oxlint (+25 more)

### Community 5 - "Component"
Cohesion: 0.10
Nodes (19): Parse a dataframe of components., Any, Convert structured dictionary rows from TableParser into Component + SKU objects, Analyze extracted components and synthesize limits (e.g. max OCP slots, risers)., Extract high-level Workloads (Customer Intent) and link to Platform., Extract processor specifications from QuickSpecs tables., Extract memory specifications., Extract storage / drive cage specifications. (+11 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.08
Nodes (15): Any, GraphBuilder, Any, Remove a concept and all its edges from the graph., Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Check if a node's attributes match all criteria. (+7 more)

### Community 7 - "App.tsx"
Cohesion: 0.10
Nodes (19): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), PlatformDashboard(), SemanticSearch() (+11 more)

### Community 8 - "models.py"
Cohesion: 0.16
Nodes (17): datetime, Enum, Source Registry — Registers, classifies, and tracks engineering sources.  Govern, PackagingType, ProcessingStatus, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, Rule severity levels., Packaging classification for components and SKUs. (+9 more)

### Community 9 - "cli.py"
Cohesion: 0.12
Nodes (20): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+12 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.15
Nodes (12): PDFExtractor, Classify a component description into (category, subcategory) using keyword scor, Stage 1: Normalize invisible PDF typography and Unicode artifacts., Returns True if the rule contains negation phrasing that should reverse/discard, Extracts engineering knowledge from vendor QuickSpecs and technical PDFs.      B, Every engineering source SHALL receive a permanent identity.     Blueprint 04 §5, Source, ingest_all() (+4 more)

### Community 12 - "RuleEngine"
Cohesion: 0.15
Nodes (10): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluates a set of component IDs against the canonical graph to ensure     all c, Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine (+2 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 15 - "._extract_platform_identity"
Cohesion: 0.14
Nodes (6): Extract product description from introductory text., Extract chassis type variants., Extract engineering capabilities mentioned in the document., Extract workload suitability tags., Fallback when automated title/vendor/domain extraction fails.          This does, Extract the main platform identity from the document using generalized heuristic

### Community 16 - "Platform"
Cohesion: 0.22
Nodes (8): Extract spatial topology and slot mappings., Platform, Spatial topology mapping for physical components., A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., SlotMapping, test_rule_engine(), test_solution_generator(), TestTopology

### Community 18 - "SourceRegistry"
Cohesion: 0.21
Nodes (7): Path, Attempt to infer vendor from filename., Registers and classifies engineering sources.     Blueprint 04 §5: Every source, Register a new engineering source file.         Assigns permanent identity, clas, Update the processing status of a source., Compute SHA-256 hash of a file for duplicate detection., SourceRegistry

### Community 19 - "conftest.py"
Cohesion: 0.20
Nodes (9): api_client(), empty_graph(), Shared pytest fixtures.  CRITICAL: tests must never point a RepoManager at the r, Create a shared temporary directory for test artifacts., Returns a clean GraphBuilder instance., A RepoManager fully isolated in a pytest tmp_path, seeded with a     minimal but, A FastAPI TestClient wired to `temp_repo` instead of the real,     on-disk proje, shared_temp_dir() (+1 more)

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.28
Nodes (4): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis

### Community 21 - "pdf_extractor.py"
Cohesion: 0.29
Nodes (4): PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Any, Parses PDF tables using pdfplumber to accurately extract SKUs,      bracketed no, TableParser

### Community 22 - "SKU"
Cohesion: 0.32
Nodes (3): A commercially orderable item.     Blueprint 03 §4: Engineering knowledge SHALL, SKU, TestFuzzyMatching

### Community 23 - "logger.py"
Cohesion: 0.33
Nodes (6): get_logger(), IKP Structured Logger — Centralized observability for the platform.  Governs: Bl, Configure a structured logger with both console and file handlers., Get a logger for a specific module., setup_logger(), Logger

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
- **84 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `PDFExtractor` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `Component`, `models.py`, `cli.py`, `._extract_platform_identity`, `Platform`, `ObsidianMCPClient`, `pdf_extractor.py`, `SKU`, `TestPlatformIdentityAgainstRealPDFs`, `._extract_rules`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `GraphBuilder` to `BaseEngineeringObject`, `EvidenceRecord`, `RepoManager`, `Component`, `PDFExtractor`, `RuleEngine`, `Platform`, `TestGraphBuilder`, `conftest.py`, `SKU`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `RepoManager` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `GraphBuilder`, `cli.py`, `PDFExtractor`, `TestGraphBuilder`, `conftest.py`, `ObsidianMCPClient`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `BaseEngineeringObject`) actually correct?**
  _`PDFExtractor` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `BaseEngineeringObject` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`BaseEngineeringObject` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Platform` (e.g. with `ExcelExtractor` and `PDFExtractor`) actually correct?**
  _`Platform` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `RepoManager` (e.g. with `ApprovalRequest` and `BOQValidationRequest`) actually correct?**
  _`RepoManager` has 20 INFERRED edges - model-reasoned connections that need verification._