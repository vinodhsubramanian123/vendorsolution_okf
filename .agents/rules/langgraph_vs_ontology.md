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

### IMPLEMENTED (The Foundation)
1.  **Ingestion Pipeline**: Automated extraction from PDF sources (`pdf_extractor.py`, `table_parser.py`). Populates the graph.
2.  **Knowledge Graph Storage**: The Open Knowledge Format (OKF) repository markdown writer and reader (`okf_writer.py`, `okf_reader.py`).
3.  **In-Memory Graph**: NetworkX-based `GraphBuilder` for fast traversal and filtering, complete with bidirectional traversal helpers (`get_related`).
4.  **Deterministic Validation**: The `RuleEngine` that traverses the graph to validate constraints, category limits, rules, and compatibility strictly within solution domains.
5.  **Semantic Search & Deduplication**: Vector storage and difflib matching to prevent duplicate rule creation.
6.  **LangGraph Orchestrator**: Implemented under `ikp_platform/core/workflow/` with bounded attempts and placeholder nodes for live portal/HITL behavior.
7.  **Customer Intent Mapping**: Implemented through `IntentParser`, using Gemini when configured and deterministic fallback behavior when it is not.
8.  **Solution Synthesis And Ranking**: Implemented through `SolutionGenerator` with profile-based candidates; pricing remains placeholder-level.

### NOT YET IMPLEMENTED OR PARTIAL
1.  **Live Partner Portal Integration**: The dynamic validation loop is a placeholder and does not call live vendor systems.
2.  **Human-in-the-Loop (HITL) Resume Flow**: Review queue support exists, but full approve/reject/resume coverage for every `KnowledgeDelta` is still partial.
3.  **Advanced Extractors**: PDF and Excel exist; portal extraction and broader vendor-specific adapters are still backlog.
4.  **Live Pricing/Availability Ranking**: Alternative estimates use static placeholders until real pricing or portal data is integrated.

Current runtime truth is maintained in `IKP/standards/11_CURRENT_IMPLEMENTATION_STACK.md`.
