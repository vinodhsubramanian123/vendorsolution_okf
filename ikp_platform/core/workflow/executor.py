"""
Workflow Executor — API/CLI entry point for running the LangGraph state machine.

Governs: LangGraph Orchestrator Pipeline
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.workflow.graph import build_workflow_graph
from ikp_platform.core.workflow.state import WorkflowState
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.observability import telemetry_trace

class WorkflowExecutor:
    """Executes customer queries against the LangGraph orchestrator."""
    
    def __init__(self, knowledge_graph: GraphBuilder, vector_store=None, mcp_client=None):
        self.knowledge_graph = knowledge_graph
        self.parser = IntentParser()
        self.generator = SolutionGenerator(knowledge_graph, vector_store, mcp_client)
        self.rule_engine = RuleEngine(knowledge_graph)
        self.app = build_workflow_graph(self.knowledge_graph, self.parser, self.generator, self.rule_engine)
        
    @telemetry_trace
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Run a user query through the end-to-end multi-step pipeline."""
        
        initial_state = WorkflowState(
            messages=[HumanMessage(content=query)],
            customer_requirements={},
            target_workload="",
            selected_platform="",
            current_bom=[],
            validation_errors=[],
            is_valid_static=False,
            portal_validation_errors=[],
            is_valid_dynamic=False,
            learned_constraints=[],
            requires_human_intervention=False,
            human_feedback="",
            ranked_solutions=[]
        )
        
        result = self.app.invoke(initial_state)
        
        return {
            "platform": result.get("selected_platform"),
            "bom": result.get("current_bom"),
            "ranked_solutions": result.get("ranked_solutions", [])
        }
