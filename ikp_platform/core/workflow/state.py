"""
Workflow State — Defines the TypedDict for the LangGraph orchestrator state.

Governs: LangGraph Orchestrator Pipeline
"""

from typing import List, Dict, Any
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage


class WorkflowState(TypedDict):
    """
    The state maintained by the LangGraph orchestrator during execution.
    """

    # Chat / Conversation
    messages: List[BaseMessage]

    # Customer Intent mapped to Ontology
    customer_requirements: Dict[str, Any]
    target_workload: str

    # Solution State
    selected_platform: str
    current_bom: List[str]
    attempt_count: int
    max_attempts: int

    # Validation (Static & Dynamic)
    validation_errors: List[str]
    is_valid_static: bool

    # --- FUTURE: Live Partner Portal Integration ---
    portal_validation_errors: List[
        Dict[str, Any]
    ]  # e.g. {"error": "Out of Stock", "type": "temporary"}
    is_valid_dynamic: bool

    # Knowledge Update & Learning
    learned_constraints: List[
        str
    ]  # Temporary/Permanent rules learned from portal failures

    # Human-In-The-Loop (HITL)
    requires_human_intervention: bool
    human_feedback: str

    # Final Output
    ranked_solutions: List[Dict[str, Any]]
