# Knowledge Transfer (KT) & Architectural Decisions

This document outlines the current strategies, technologies, and future roadmap considerations for the IKP (Intelligent Knowledge Platform). It explicitly clarifies *who* is doing *what* across ingestion, search, and recovery workflows to eliminate all ambiguity.

---

## 1. Responsibility Matrix (Who Does What & How)

The following table explicitly defines the roles, technologies, and actors across the three main phases of the platform lifecycle:

| Lifecycle Phase | Component / Actor | Role & Mechanism (How it works) | Technology Used (Current) | Future Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **1. Source Ingestion** | **Google Gemini (LLM)** | Extracts structured components and rules from raw PDFs *at start time*. | Gemini API (`pdf_extractor.py`) | *No change* |
| **1. Source Ingestion** | **Fingerprinter** | Computes MD5/SHA256 of extracted objects. If they change, it generates a `KnowledgeDelta`. | Python `hashlib` (`version_tracker.py`) | *No change* |
| **1. Source Ingestion** | **Canonical Storage** | Saves extracted components as Markdown (`.md`) files on disk. | Local Filesystem (`OKFWriter`) | *No change* |
| **1. Source Ingestion** | **Indexer** | Embeds the Markdown files and saves them into the vector database. | **ChromaDB** (`VectorStore`) | *No change* |
| **2. Search (API)** | **Semantic Search Engine** | Looks up the query in the vector DB to find fuzzy/conceptual matches. | **ChromaDB** (Internal) | *No change* |
| **2. Search (API)** | **Graph Search Engine** | Looks up explicit relationships (e.g., "Compatible With") to boost search scores. | **NetworkX** (In-Memory Python Graph) | Migrate to **Neo4j** |
| **2. Search (Actors)** | **Google AI Studio / CLI** | **Clients** that call our `/api/search` endpoint to retrieve data. They *consume* search; they do not *index*. | REST API / HTTP Clients | *No change* |
| **3. Recovery / Sync** | **Obsidian MCP Client** | Acts as a client to an *external* Partner Portal MCP Server to fetch missing rules or alternative SKUs. | MCP Protocol (`mcp_client.py`) | *No change* |
| **3. Recovery / Sync** | **Human Reviewer** | Validates delta changes or submits explicit corrections via `/api/feedback`. | REST API (`feedback_template.py`) | *No change* |
| **3. Recovery / Sync** | **Error Resolution Agent** | Diagnoses obscure Partner Portal errors (e.g., "PCI Bandwidth Exceeded"). | *None currently (manual)* | Build orchestrator using **LlamaIndex** |

---

## 2. Clarifying Current Confusions

To ensure project schemas and Agent instructions are fully aligned, here are explicit clarifications regarding recent questions:

### A. Is Google AI Studio or Antigravity CLI helping in search?
**NO.** Google AI Studio (acting as a reasoning agent) and the Antigravity CLI are **Clients**. They do not power the search indexing or execution. They simply send an HTTP `POST` request to our `/api/search` endpoint, and our internal backend (FastAPI + ChromaDB + NetworkX) does the actual searching.

### B. How does the "In-Memory NetworkX Graph" work? Is it Semantic or Normal Search?
*   **What it is:** NetworkX is a standard Python library running in the RAM of our FastAPI server. It is **NOT** a database and it is **NOT** semantic.
*   **How it works (Normal/Structural Search):** It stores explicit, hard-coded relationships (e.g., `Node A` is connected to `Node B` via a `COMPATIBLE_WITH` edge).
*   **Who does it:** The `repo_manager.py` (specifically the `search()` function) queries this graph.
*   **Role in Search:** After ChromaDB returns semantic results, `repo_manager.py` looks at the NetworkX graph. If it sees that a semantic result is *structurally* connected to the platform the user is querying, it artificially boosts the search score (`+0.2`).

### C. Are we reading PDFs during search time?
**ABSOLUTELY NOT.** 
Reading PDFs at search time (runtime) is far too slow. 
*   During **Ingestion (Start Time)**: We read the PDFs, use LLMs to extract data, save that data as lightweight `.md` files, and index them into ChromaDB.
*   During **Search (Run Time)**: We *only* query ChromaDB and the NetworkX graph. The original PDFs are never touched during a search query.

### D. Does LlamaIndex help during search or ingestion?
**Currently, we DO NOT use LlamaIndex anywhere in the platform.** 
My previous notes about LlamaIndex were **Future Recommendations** for the *Recovery Workflow*. We do not maintain a LlamaIndex table during ingestion. All vector embedding and searching is currently handled natively by **ChromaDB**.

---

## 3. Future Roadmap: Neo4j & LlamaIndex for Recovery Workflows

When the Partner Portal rejects our generated BOM (Bill of Materials) with complex errors, we enter the **Recovery Flow**. This is where our current in-memory architecture (NetworkX) will struggle to scale, and where we must upgrade.

### A. Neo4j for Graph Constraints & Pathfinding (The SKU Matcher)
*   **Role in Recovery:** Neo4j is an enterprise Graph Database. If the partner portal rejects a SKU, we query Neo4j using Cypher (`MATCH (failed_sku)-[:COMPATIBLE_WITH]-(alternative_sku) RETURN alternative_sku`) to mathematically guarantee a compatible replacement.
*   **Why it replaces NetworkX:** NetworkX cannot handle tens of thousands of complex traversal queries efficiently. Neo4j acts as the strict, deterministic "SKU Matcher".

### B. LlamaIndex for RAG-based Error Resolution (The Fuzzy Matcher)
*   **Role in Recovery:** When the Partner Portal returns an unstructured, obscure error (e.g., `ERR_PCI_BNDW_EXCEEDED`), we cannot use Neo4j because it's not a graph issue—it's a knowledge interpretation issue. 
*   **How it would work:** We would deploy LlamaIndex *as a dedicated RAG agent*. It would read the existing `.md` files (not the PDFs) to find the specific PCI lane limit documentation and synthesize a plain-English explanation of why the error occurred.

### Summary of Future Weighting Strategy (Hybrid RRF)
When resolving a Partner Portal conflict, our system must weigh conflicting information using **Reciprocal Rank Fusion (RRF)**:
1.  **Human Feedback Deltas (100% Weight):** An explicit correction submitted via `/api/feedback` is absolute truth.
2.  **SKU Match via Graph / Neo4j (80% Weight):** Structural compatibility bounds. If the graph says it fits, it gets a massive ranking priority.
3.  **Semantic / Fuzzy Match via ChromaDB / LlamaIndex (20% Weight):** Used primarily as a fallback to interpret unstructured error messages when the exact SKU match isn't obvious.

---

## 4. Search Architecture Schema

```mermaid
graph TD
    %% 1. Ingestion Phase (Start Time)
    subgraph Ingestion Phase
        PDF[Raw PDFs] -->|Extracted by Gemini| MD[Canonical .md Files]
        MD -->|Embedded| VDB[(ChromaDB Vector Store)]
        MD -->|Parsed| G[(NetworkX In-Memory Graph)]
    end

    %% 2. Execution Phase (Search Time)
    subgraph Internal Search Engine
        VDB -->|Semantic Score| RM[RepoManager Hybrid Search]
        G -->|Structural Boost| RM
        RM -->|JSON Results| API[/api/search Endpoint]
    end

    %% 3. The Clients (Consumers)
    subgraph The Clients
        AI[Google AI Studio / Solution Gen] -->|HTTP GET/POST| API
        UI[Antigravity CLI / Human User] -->|HTTP GET/POST| API
    end

    %% 4. Recovery & Sync Phase
    subgraph Phase 6 Vendor Portal
        MCPClient[Obsidian MCP Client mcp_client.py]
        API -.->|Fallback Sync| MCPClient
        MCPClient -->|Queries| ExtVault[Vendor Markdown Vault]
    end
```
