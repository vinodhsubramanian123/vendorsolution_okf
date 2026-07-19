---
name: LangGraph Workflow vs Knowledge Graph Ontology
description: Architectural rules defining the boundary between static knowledge (ontology nodes/edges) and dynamic AI workflows (LangGraph nodes/edges), and current implementation status.
---

# Architecture: Knowledge Graph vs LangGraph

To prevent severe architectural and terminology confusion during AI development sessions, you MUST maintain a strict boundary between the **Knowledge Graph** (the static data) and the **LangGraph Workflow** (the dynamic process).

## 1. The Knowledge Graph (The "What")
The Knowledge Graph represents static, verified engineering truths. It has no awareness of a "customer", a "session", or an "active workflow".

*   **Ontology Nodes**: The physical or conceptual building blocks (`BaseEngineeringObject` subclasses in `models.py`).
    *   Examples: `Platform`, `Component`, `SKU`, `Constraint`, `CategoryLimit`, `Workload`, `Rule`.
*   **Ontology Edges**: The direct technical relationships (`EngineeringRelationship`) connecting building blocks.
    *   Examples: `Contains`, `CompatibleWith`, `Requires`, `IncompatibleWith`, `HasSKU`, `Supports`.

*Rule of thumb: The Knowledge Graph dictates what is technically POSSIBLE.*

## 2. The LangGraph Workflow (The "How")
LangGraph represents the dynamic orchestration pipeline that queries the Knowledge Graph to build a solution for a specific customer.

*   **Process Nodes**: Python functions or AI agents in the LangGraph state machine.
    *   Examples: `parse_customer_intent`, `generate_bom`, `validate_with_rule_engine`, `rank_top_skus`.
*   **Process Edges**: Conditional logic paths determining which agent/function runs next based on the workflow state.
    *   Examples: `if bom_is_valid -> rank_solutions`, `if bom_invalid -> regenerate_bom`.

*Rule of thumb: The LangGraph Workflow dictates what is OPTIMAL.*

---

## 3. Current Implementation Status

As we continue development, refer to this checklist to understand what parts of the multi-step solution are complete versus pending.

### ✅ IMPLEMENTED (The Foundation)
1.  **Ingestion Pipeline**: Automated extraction from PDF sources (`pdf_extractor.py`, `table_parser.py`). Populates the graph.
2.  **Knowledge Graph Storage**: The Open Knowledge Format (OKF) repository markdown writer and reader (`okf_writer.py`, `okf_reader.py`).
3.  **In-Memory Graph**: NetworkX-based `GraphBuilder` for fast traversal and filtering, complete with bidirectional traversal helpers (`get_related`).
4.  **Deterministic Validation**: The `RuleEngine` that traverses the graph to validate constraints, category limits, rules, and compatibility strictly within solution domains.
5.  **Semantic Search & Deduplication**: Vector storage and difflib matching to prevent duplicate rule creation.

### ❌ NOT YET IMPLEMENTED (The Next Steps)
1.  **The LangGraph Orchestrator**: The actual LangGraph state machine, nodes, and edges that drive the multi-step AI workflow. Currently, we just have the underlying reasoning tools.
2.  **Customer Intent Mapping**: The pipeline step that takes unstructured customer requests and maps them to `Workload` nodes to begin the traversal.
3.  **SKU Ranking System**: The logic to generate 5 valid solutions and rank them based on non-technical customer preferences (budget, vendor, etc.) by traversing `HasSKU` edges.
4.  **Advanced Ingestion Extractors**: The Excel and Portal parsers needed to dynamically extract `Variant`, `SolutionCategory`, and `Configuration` objects (flagged in the audit).
5.  **Live Partner Portal Integration**: The dynamic validation loop that checks a statically-valid BOM against live vendor APIs for global supply chain limits, temporary/permanent error classification, and Knowledge Graph updates (see placeholders in `ikp_platform/core/workflow/nodes.py`).
6.  **Human-in-the-Loop (HITL)**: Workflow pausing for engineer intervention during difficult vendor API rejections or unresolvable cyclic constraints.

When you build out the LangGraph components, place them in a dedicated workflow directory (e.g., `ikp_platform/core/workflow/`) to keep the separation of concerns absolute.
