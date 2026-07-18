# Graph Report - vendorsolution_okf  (2026-07-18)

## Corpus Check
- 80 files · ~35,217 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 713 nodes · 1553 edges · 58 communities (40 shown, 18 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 286 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8ea94a60`
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
- list_models.py
- SlotMapping
- BaseModel
- .reindex_vector_store
- .update_context
- api_client
- shared_temp_dir
- temp_dir
- BaseEngineeringObject
- GraphBuilder

## God Nodes (most connected - your core abstractions)
1. `GraphBuilder` - 50 edges
2. `PDFExtractor` - 43 edges
3. `RepoManager` - 42 edges
4. `TestGraphBuilder` - 41 edges
5. `BaseEngineeringObject` - 36 edges
6. `Platform` - 35 edges
7. `TestOntologyModels` - 34 edges
8. `TestOKFWriter` - 34 edges
9. `Source` - 32 edges
10. `OKFWriter` - 31 edges

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

## Communities (58 total, 18 thin omitted)

### Community 0 - "BaseEngineeringObject"
Cohesion: 0.11
Nodes (26): datetime, BaseEngineeringObject, Configuration, Constraint, EngineeringRelationship, IKP Canonical Engineering Ontology — Complete Model Definitions  Governs: Bluepr, A directed, typed, evidence-backed relationship between two engineering objects., The canonical base for all engineering knowledge.     Blueprint 03 §4: Every eng (+18 more)

### Community 1 - "EvidenceRecord"
Cohesion: 0.14
Nodes (25): ABC, Excel Source Parser — Extracts engineering objects from structured spreadsheets., ConfidenceLevel, DeltaChange, DeltaChangeType, EvidenceRecord, KnowledgeDelta, Types of changes a Knowledge Delta can contain. (+17 more)

### Community 2 - "IntentParser"
Cohesion: 0.09
Nodes (15): LLMClient, Any, LLM Client — Centralized Gemini Integration  Governs: Dynamic Intent Parsing and, Generate vector embeddings for a list of strings., Ask Gemini via local Antigravity CLI to extract explicit engineering rules from, Wrapper for the Gemini LLM API., Ask Gemini via local Antigravity CLI to find edge-case constraints or subtle dep, Ask Gemini to parse natural language intent into structured JSON. (+7 more)

### Community 3 - "RepoManager"
Cohesion: 0.09
Nodes (26): cmd_ingest(), cmd_learn(), cmd_mcp(), cmd_query(), cmd_scan(), cmd_status(), cmd_validate(), main() (+18 more)

### Community 4 - "devDependencies"
Cohesion: 0.06
Nodes (33): axios, dependencies, axios, lucide-react, react, react-dom, devDependencies, oxlint (+25 more)

### Community 5 - "Component"
Cohesion: 0.08
Nodes (26): DataFrame, ExcelExtractor, Parse a dataframe of components., Parse a dataframe of SKUs., Parses Excel spreadsheets into IKP canonical objects., Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta)., Path, Source Registry — Registers, classifies, and tracks engineering sources.  Govern (+18 more)

### Community 6 - "GraphBuilder"
Cohesion: 0.09
Nodes (15): Rule Engine — Deterministic constraint and compatibility evaluation.  Governs: B, GraphBuilder, BaseEngineeringObject, Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.  Gov, Remove a concept and all its edges from the graph., Find all nodes that have ALL the required capabilities., Find all nodes of a given type., Maintains an in-memory NetworkX DiGraph representing the canonical     engineeri (+7 more)

### Community 7 - "App.tsx"
Cohesion: 0.10
Nodes (19): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, BoqValidation(), PlatformDashboard(), SemanticSearch() (+11 more)

### Community 8 - "models.py"
Cohesion: 0.09
Nodes (18): ObsidianMCPClient, Client for interacting with the Obsidian MCP server (seekstone).     Provides pa, Whether the seekstone binary can actually be found on PATH., Synchronous wrapper to execute a search against the vault.         Returns a lis, OKFReader, Any, BaseEngineeringObject, Path (+10 more)

### Community 9 - "cli.py"
Cohesion: 0.13
Nodes (13): IntentParser, Intent Parser — Extracts structured engineering requirements from natural langua, Parses unstructured customer intent into a structured CustomerRequest.     V1.0, Parse natural language into a structured request using LLM., Solution Generator — Synthesizes optimized solution candidates.  Governs: Bluepr, call_tool(), list_tools(), List available tools. (+5 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 11 - "PDFExtractor"
Cohesion: 0.25
Nodes (5): Any, Path, Generate an index.md for the given directory listing all .md concepts.         O, Append an entry to log.md in OKF §7 format.         Date headings use ISO 8601 Y, Read YAML frontmatter from an OKF Markdown file.

### Community 12 - "RuleEngine"
Cohesion: 0.15
Nodes (9): Evaluate platform constraints (e.g., max memory, max drives, category limits)., Check if all required dependencies are present in the solution., Evaluate applicable engineering rules., Evaluates a set of component IDs against the canonical graph to ensure     all c, Evaluate if a solution is valid.         Returns: (is_valid, reasoning_chain, er, Check if all components are compatible with the platform, enforcing STRICT Solut, RuleEngine, Any (+1 more)

### Community 13 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 14 - "Setup"
Cohesion: 0.12
Nodes (14): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Agent Configuration, Cross-Platform Toolchain Setup, Vendorsolution OKF, 1. Prerequisites, 2. Install, 3. Configure environment (+6 more)

### Community 15 - "._extract_platform_identity"
Cohesion: 0.05
Nodes (43): Component, EngineeringRelationship, EvidenceRecord, PDFExtractor, Any, BaseEngineeringObject, PDF Extractor — Extracts engineering knowledge from vendor PDF documents.  Gover, Classify a component description into (category, subcategory) using keyword scor (+35 more)

### Community 16 - "Platform"
Cohesion: 0.11
Nodes (17): Learning Engine — Merges Knowledge Deltas into the canonical repository.  Govern, DeltaStatus, Knowledge Delta lifecycle status., Repository Manager — Orchestrates bidirectional sync between OKF files and the i, Apply a validated Knowledge Delta — persist all objects and record the delta., Update STATE.md with current platform statistics., Append an entry to the project root LOG.md., Record a Knowledge Delta in the history/ directory. (+9 more)

### Community 18 - "SourceRegistry"
Cohesion: 0.15
Nodes (15): CustomerRequest, CustomerRequirement, EngineeringAttribute, HistoryEntry, BaseModel, Immutable change record for an engineering object.     Blueprint 06 §7: "Never o, A typed, structured engineering attribute., A single structured requirement extracted from a customer request. (+7 more)

### Community 19 - "Platform"
Cohesion: 0.19
Nodes (9): Platform, A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)., OKFWriter, Generate structured markdown body with capabilities, relationships, and evidence, Writes a single engineering concept to disk as an OKF Markdown file.         Ret, Writes engineering knowledge to disk in OKF format., Derive hierarchical file path from the object's ontological position.          B, Convert a string to a filesystem-safe slug. (+1 more)

### Community 20 - "ObsidianMCPClient"
Cohesion: 0.20
Nodes (14): Enum, EngineeringObjectType, LifecycleStatus, PackagingType, Product lifecycle status for engineering objects., Rule severity levels., Packaging classification for components and SKUs., Canonical hierarchy levels from Blueprint 03 §3. (+6 more)

### Community 21 - "LearningEngine"
Cohesion: 0.14
Nodes (8): LearningEngine, Human approves a pending delta.         Blueprint 02 §10: Approved decisions bec, Reject a pending delta with a reason., Get all deltas awaiting human review., Determine if a delta can be auto-approved based on confidence.         Conservat, Accepts Knowledge Deltas from any source and merges validated changes     into t, Submit a Knowledge Delta for review.         Deltas with sufficient confidence m, Merge all validated deltas into the canonical repository.         Returns the nu

### Community 22 - "SKU"
Cohesion: 0.23
Nodes (18): BaseModel, ApprovalRequest, approve_object(), BOQValidationRequest, get_repo(), get_review_queue(), get_status(), query_solution() (+10 more)

### Community 23 - "BOQValidator"
Cohesion: 0.19
Nodes (6): BOQValidator, Validates a Bill of Quantities against the canonical catalog,     using fuzzy ma, Attempts to match a requested SKU against catalog SKUs.         Returns (matched, TestFuzzyMatching, ValidationResult, VendorValidator

### Community 24 - "Component"
Cohesion: 0.33
Nodes (5): CategoryLimit, Component, A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).     Bl, A constraint specifically targeting a maximum or minimum quantity for a category, TestCategoryLimits

### Community 25 - "Coverage"
Cohesion: 0.33
Nodes (5): Coverage, IKP Engineering Context, Learnings & Architecture Updates (Agent Run), Solution Domains, Sources Ingested: 1

### Community 26 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

### Community 27 - ".filter_by_metadata"
Cohesion: 0.25
Nodes (5): Any, Filter nodes by metadata attributes.          Blueprint 05 §6: "Before reasoning, Check if a node's attributes match all criteria., Traverse relationships from a node, optionally filtered by type.          Bluepr, Get all objects compatible with the given object.

### Community 28 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 47 - "list_models.py"
Cohesion: 0.47
Nodes (4): CustomerRequest, Builds a single candidate and validates it., Generate multiple solution profiles.         Blueprint 05 §13: Where appropriate, SolutionCandidate

### Community 49 - "SlotMapping"
Cohesion: 0.60
Nodes (3): Spatial topology mapping for physical components., SlotMapping, TestTopology

## Knowledge Gaps
- **84 isolated node(s):** `Solution Domains`, `Sources Ingested: 1`, `Learnings & Architecture Updates (Agent Run)`, `Knowledge Graph Statistics`, `Objects by Type` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PDFExtractor` connect `._extract_platform_identity` to `RepoManager`, `RuleEngine`, `Component`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `GraphBuilder` connect `GraphBuilder` to `BaseEngineeringObject`, `models.py`, `cli.py`, `RuleEngine`, `Platform`, `TestGraphBuilder`, `SourceRegistry`, `Platform`, `ObsidianMCPClient`, `SKU`, `BOQValidator`, `Component`, `.filter_by_metadata`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `RepoManager` connect `Platform` to `BaseEngineeringObject`, `EvidenceRecord`, `IntentParser`, `RepoManager`, `GraphBuilder`, `models.py`, `cli.py`, `TestGraphBuilder`, `SourceRegistry`, `Platform`, `.reindex_vector_store`, `LearningEngine`, `.update_context`, `ObsidianMCPClient`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `GraphBuilder` (e.g. with `RuleEngine` and `SolutionGenerator`) actually correct?**
  _`GraphBuilder` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `PDFExtractor` (e.g. with `TableParser` and `TestIngestion`) actually correct?**
  _`PDFExtractor` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `RepoManager` (e.g. with `LearningEngine` and `BaseEngineeringObject`) actually correct?**
  _`RepoManager` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `TestGraphBuilder` (e.g. with `BaseEngineeringObject` and `Component`) actually correct?**
  _`TestGraphBuilder` has 28 INFERRED edges - model-reasoned connections that need verification._