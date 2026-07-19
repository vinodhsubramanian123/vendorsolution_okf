"""
Workflow Graph — Defines the LangGraph state machine structure and conditional edges.

Governs: LangGraph Orchestrator Pipeline
"""

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from ikp_platform.core.workflow.state import WorkflowState
from ikp_platform.core.workflow.nodes import WorkflowNodes
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
import logging

logger = logging.getLogger("ikp.workflow.graph")


def should_loop_bom(state: WorkflowState) -> str:
    """Conditional edge router based on BOM validation with bounded retries."""
    if state.get("is_valid_static", False):
        logger.info("Routing from validate_bom -> live_portal_validation (Valid static BOM)")
        return "live_portal_validation"

    attempt_count = state.get("attempt_count", 0)
    max_attempts = state.get("max_attempts", 3)

    if attempt_count >= max_attempts:
        logger.warning(f"Routing from validate_bom -> human_intervention (Max attempts {attempt_count} reached)")
        return "human_intervention"

    logger.info(f"Routing from validate_bom -> draft_bom (Attempt {attempt_count} failed, retrying)")
    return "draft_bom"


def should_human_intervene(state: WorkflowState) -> str:
    """Conditional edge router for portal validation failures."""
    if state.get("is_valid_dynamic", False):
        logger.info("Routing from live_portal_validation -> rank_solutions (Portal validation passed)")
        return "rank_solutions"
    elif state.get("requires_human_intervention", False):
        logger.warning("Routing from live_portal_validation -> human_intervention (Portal rejected permanently)")
        return "human_intervention"
    else:
        logger.info("Routing from live_portal_validation -> update_knowledge_base (Portal rejected temporarily)")
        return "update_knowledge_base"


def build_workflow_graph(
    knowledge_graph: GraphBuilder,
    parser: IntentParser,
    generator: SolutionGenerator,
    rule_engine: RuleEngine,
) -> CompiledStateGraph:
    """Builds and wires the LangGraph StateMachine."""

    workflow_nodes = WorkflowNodes(knowledge_graph, parser, generator, rule_engine)
    workflow = StateGraph(WorkflowState)

    workflow.add_node("parse_intent", workflow_nodes.parse_intent)
    workflow.add_node("select_platform", workflow_nodes.select_platform)
    workflow.add_node("draft_bom", workflow_nodes.draft_bom)
    workflow.add_node("validate_bom", workflow_nodes.validate_bom)
    workflow.add_node("live_portal_validation", workflow_nodes.live_portal_validation)
    workflow.add_node("update_knowledge_base", workflow_nodes.update_knowledge_base)
    workflow.add_node("human_intervention", workflow_nodes.human_intervention)
    workflow.add_node("rank_solutions", workflow_nodes.rank_solutions)

    workflow.set_entry_point("parse_intent")
    workflow.add_edge("parse_intent", "select_platform")
    workflow.add_edge("select_platform", "draft_bom")
    workflow.add_edge("draft_bom", "validate_bom")

    workflow.add_conditional_edges(
        "validate_bom",
        should_loop_bom,
        {
            "live_portal_validation": "live_portal_validation", 
            "draft_bom": "draft_bom",
            "human_intervention": "human_intervention"
        },
    )

    workflow.add_conditional_edges(
        "live_portal_validation",
        should_human_intervene,
        {
            "rank_solutions": "rank_solutions",
            "update_knowledge_base": "update_knowledge_base",
            "human_intervention": "human_intervention",
        },
    )

    workflow.add_edge("update_knowledge_base", "draft_bom")
    workflow.add_edge("human_intervention", END)
    workflow.add_edge("rank_solutions", END)

    return workflow.compile()
