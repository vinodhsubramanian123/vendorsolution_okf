"""
Workflow Executor — API/CLI entry point for running the LangGraph state machine.

Governs: LangGraph Orchestrator Pipeline
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.workflow.graph import build_workflow_graph
from ikp_platform.core.workflow.state import WorkflowState
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.observability import telemetry_trace
import logging

logger = logging.getLogger("ikp.workflow.executor")


class WorkflowExecutor:
    """Executes customer queries against the LangGraph orchestrator."""

    def __init__(
        self, knowledge_graph: GraphBuilder, vector_store=None, mcp_client=None
    ):
        self.knowledge_graph = knowledge_graph
        self.parser = IntentParser()
        self.generator = SolutionGenerator(knowledge_graph, vector_store, mcp_client)
        self.rule_engine = RuleEngine(knowledge_graph)
        self.app = build_workflow_graph(
            self.knowledge_graph, self.parser, self.generator, self.rule_engine
        )

    @telemetry_trace
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Run a user query through the end-to-end multi-step pipeline."""

        initial_state = WorkflowState(
            messages=[HumanMessage(content=query)],
            customer_requirements={},
            target_workload="",
            selected_platform="",
            current_bom=[],
            attempt_count=0,
            max_attempts=3,
            validation_errors=[],
            validation_failures=[],
            is_valid_static=False,
            excluded_component_ids=[],
            tried_candidate_indices=[],
            needs_regeneration=False,
            portal_validation_errors=[],
            is_valid_dynamic=False,
            learned_constraints=[],
            requires_human_intervention=False,
            human_feedback="",
            human_review_payload={},
            recovery_audit_trail=[],
            ranked_solutions=[],
            visited_bom_hashes=[],
            cycle_detected=False,
        )

        logger.info(f"Starting LangGraph workflow execution for query: '{query[:50]}...'")
        result = self.app.invoke(initial_state)
        
        platform_result = result.get("selected_platform")
        bom_result = result.get("current_bom", [])
        logger.info(f"LangGraph execution completed. Platform: {platform_result}, BOM size: {len(bom_result)}")

        return {
            "platform": platform_result,
            "bom": bom_result,
            "ranked_solutions": result.get("ranked_solutions", []),
            "requires_human_intervention": result.get("requires_human_intervention", False),
            "human_review_payload": result.get("human_review_payload", {}),
            "customer_requirements": result.get("customer_requirements", {}),
            "attempt_count": result.get("attempt_count", 0),
            "cycle_detected": result.get("cycle_detected", False),
            "visited_bom_hashes": result.get("visited_bom_hashes", []),
        }
