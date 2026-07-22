# Knowledge Transfer (KT) & Architectural Decisions

This document outlines the current strategies, technologies, and future roadmap considerations for the IKP (Intelligent Knowledge Platform). It serves as a definitive reference for how the platform handles ingestion, search, fingerprinting, and complex reasoning.

---

## 1. Indexing & Fingerprinting Strategy

### Current Strategy (What we are using)
We are **not** using LlamaIndex for our core ingestion and indexing pipeline. Instead, we use a bespoke, dual-layer architecture tailored for strict engineering governance:
1.  **Canonical Repository (Source of Truth):** When PDFs are ingested (via `HPEQuickSpecsAdapter` leveraging Google Gemini models for structured extraction), the extracted entities are mapped to `BaseEngineeringObject` models and written as **Markdown files** (`.md`) inside the `repository/` folder. This is our Canonical OKF (Open Knowledge Format).
2.  **Fingerprinting:** We do not use ambiguous tracking mechanisms. Fingerprinting is deterministic. `version_tracker.py` computes an MD5 checksum of the source PDF, and a SHA-256 hash of the extracted canonical JSON objects. If a PDF is re-ingested and the extracted data changes, a `KnowledgeDelta` is explicitly generated and recorded in the `manifest.json`.
3.  **Vector Indexing:** The canonical Markdown objects are parsed by `OKFReader` and ingested into **ChromaDB** directly (via our `VectorStore` class in `vector_store.py`). We use ChromaDB to generate embeddings (e.g., via `all-MiniLM-L6-v2`) for fast semantic retrieval.

*In short: We use a custom pipeline (Gemini extraction → Canonical Markdown OKF → ChromaDB), completely bypassing LlamaIndex for indexing to maintain absolute control over the data lifecycle and versioning.*

---

## 2. Search & Retrieval Architecture (Who & How)

There is a critical distinction between our **Internal Canonical Search** and our **External Fallback Search**.

### A. How Internal Search Works on our `.md` files
Our core intelligence lives in the generated Markdown (`.md`) files inside the `repository/` folder. 
1. **Indexing:** `VectorStore` (using ChromaDB) automatically ingests the content and metadata of these `.md` files, generating vector embeddings (e.g., via `all-MiniLM-L6-v2`) for fast semantic retrieval.
2. **Hybrid Execution:** When a query hits `/api/search`, `repo_manager.py` executes a **Hybrid Search**. It first queries ChromaDB for semantic similarity, and then applies a graph boost using the `NetworkX` in-memory graph (e.g., boosting scores by `+0.2` or `+0.3` if there's an exact platform/category match).

### B. Who is doing the Search? (The Actors)
The internal Hybrid Search is exposed via our REST API (`/api/search`). The following actors query it:
1. **Google AI Studio / Reasoning LLMs:** Our internal agentic pipelines query this endpoint to find compatible components when building a Bill of Materials (BOM) in `solution_generator.py`.
2. **Antigravity CLI & Web UI:** Human engineers and operators querying the catalog directly.

### C. The Obsidian MCP Server (External Integration)
**We DO NOT use Obsidian MCP for our internal catalog search.** 
Instead, we implemented an **Obsidian MCP Client** (`mcp_client.py` using the `seekstone` binary) as part of our **Phase 6 Vendor Portal Integration**. 
- **What it does:** Our platform acts as a *client* connecting to an *external* Obsidian MCP server (representing a vendor's or partner's external knowledge base). 
- **Why we use it:** If our internal search fails or a component is flagged as incompatible by the Partner Portal, we query the Obsidian MCP server to retrieve the latest rules or alternative SKUs from the vendor's markdown vault, turning the results into `KnowledgeDelta` feedback loops.

### Search Architecture Schema

```mermaid
graph TD
    %% Internal Pipeline
    subgraph IKP Internal Platform
        MD[Canonical .md Files] -->|Parsed & Embedded| VDB[(ChromaDB Vector Store)]
        MD -->|Parsed| G[(NetworkX In-Memory Graph)]
        VDB -->|Semantic Score| RM[RepoManager Hybrid Search]
        G -->|Graph Boost| RM
        RM -->|JSON Results| API[/api/search Endpoint]
    end

    %% The Actors querying our API
    subgraph The Actors
        AI[AI Reasoning / Solution Gen] -->|Queries| API
        UI[Human / CLI / Web UI] -->|Queries| API
    end

    %% External MCP Integration
    subgraph Phase 6 Vendor Portal
        MCPClient[Obsidian MCP Client mcp_client.py]
        API -.->|Fallback / Health Check| MCPClient
        MCPClient -->|MCP Protocol| ExtObsidian[External Obsidian MCP Server seekstone]
        ExtObsidian -->|Queries| ExtVault[Vendor Markdown Vault]
    end
```

#### Hybrid Ranking & Reciprocal Rank Fusion (RRF)
Currently, our search algorithm uses a **weighted linear combination** (a simplified form of hybrid fusion), not strict RRF, but the conceptual goal is identical:
- **Semantic Score (Base Weight):** ChromaDB returns a semantic distance score based on fuzzy/conceptual matching. This gets the highest initial weight.
- **Graph Boost (Contextual Weight):** If the retrieved node shares an explicit structural relationship in the in-memory graph (e.g., `Connected To` or `Compatible With` a requested `platform_id`), it receives a static score boost (`+0.2`).
- **Exact Metadata Match (SKU / Category Weight):** If the query has structured metadata requirements (e.g., `category="Storage"`), exact matches in the node attributes provide a heavy boost (`+0.3`) to ensure precision over fuzzy semantics.

*Future Enhancement:* We should transition from simple linear boosting to true **Reciprocal Rank Fusion (RRF)**. RRF will rank semantic results (ChromaDB) and exact SKU matches (Elasticsearch/SQL) in isolated lists, then fuse them using `score = 1 / (k + rank)`, eliminating the need to manually tune arbitrary boost constants (`+0.2`, `+0.3`).

---

## 3. Future Roadmap: Neo4j & LlamaIndex for Recovery Workflows

The platform currently uses an in-memory `NetworkX` graph. However, for solving the **Recovery Workflow** (understanding partner portal errors, finding alternative SKUs, dropping/adding components dynamically, validating entire BOMs against compatibility constraints), we need more powerful reasoning engines.

### My Architectural Views & Recommendations

#### A. Neo4j for Graph Constraints & Pathfinding
**Recommendation: HIGHLY RECOMMENDED**
- **Why:** `NetworkX` is an in-memory toy. When the catalog scales to tens of thousands of inter-dependent SKUs with complex rules (e.g., "If Chassis is 24SFF, Storage Controller must support 24 NVMe lanes"), we need an enterprise graph database.
- **Recovery Workflow:** Neo4j allows us to write Cypher queries for pathfinding. If a SKU fails in the partner portal, we can query Neo4j: `MATCH (failed_sku)-[:COMPATIBLE_WITH]-(alternative_sku) RETURN alternative_sku`. This provides deterministic, mathematically verifiable alternatives rather than relying on LLM hallucinations.
- **Validation:** Neo4j enables ACID-compliant constraint validation *before* we push a BOM to the partner portal.

#### B. LlamaIndex for RAG-based Error Resolution
**Recommendation: RECOMMENDED FOR SPECIFIC WORKFLOWS**
- **Why:** While we don't need LlamaIndex for basic ingestion, it excels at orchestrating complex RAG (Retrieval-Augmented Generation) pipelines.
- **Recovery Workflow:** When the Partner Portal returns an obscure error string (e.g., `ERR_PCI_BNDW_EXCEEDED`), LlamaIndex can be deployed to semantically search our corpus of ingested engineering manuals, retrieve the specific PCI lane limit documentation, and synthesize a resolution plan.
- **Feedback Loop Weighting:** If we adopt LlamaIndex, we should use it as an "Agentic Orchestrator". In the hybrid search model, the Neo4j Graph traversal should have the **highest weight** (because it is deterministic truth), while LlamaIndex semantic suggestions should serve as a **fallback weight** for fuzzy reasoning. 

### Summary of Future Weighting Strategy
When resolving a Partner Portal conflict:
1.  **SKU Match (Graph / Neo4j):** Weight = 80% (Deterministic truth, strict compatibility bounds).
2.  **Human Feedback Deltas:** Weight = 100% (Absolute override, applied immediately via our Phase 6 `/api/feedback` loop).
3.  **Semantic / Fuzzy Match (Vector / LlamaIndex):** Weight = 20% (Used only when the graph is sparse or for interpreting unstructured error messages).
