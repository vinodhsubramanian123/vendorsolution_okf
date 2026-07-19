"""
Workflow Nodes — Defines the executable agents and functions for LangGraph.

Governs: LangGraph Orchestrator Pipeline
"""

import logging
from typing import Dict, Any

from ikp_platform.core.workflow.state import WorkflowState
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.observability import telemetry_trace
from ikp_platform.core.ontology.models import CustomerRequest, CustomerRequirement

logger = logging.getLogger("ikp.workflow.nodes")


class WorkflowNodes:
    """Encapsulates the process nodes for the LangGraph state machine."""

    def __init__(
        self,
        graph: GraphBuilder,
        parser: IntentParser,
        generator: SolutionGenerator,
        rule_engine: RuleEngine,
    ):
        self.graph = graph
        self.parser = parser
        self.generator = generator
        self.rule_engine = rule_engine

    @telemetry_trace
    def parse_intent(self, state: WorkflowState) -> Dict[str, Any]:
        """Parse the unstructured customer message into strict requirements."""
        messages = state.get("messages", [])
        last_msg = str(messages[-1].content) if messages and hasattr(messages[-1], "content") else str(messages[-1]) if messages else ""
        parsed_request = self.parser.parse_request(last_msg)

        requirements = [r.model_dump() for r in parsed_request.requirements]

        return {
            "target_workload": parsed_request.workloads[0]
            if parsed_request.workloads
            else "Unknown",
            "customer_requirements": {
                "parsed": requirements,
                "request_id": parsed_request.request_id,
                "vendor_preference": parsed_request.vendor_preference,
            },
            "current_bom": [],
            "validation_errors": [],
            "is_valid_static": False,
            "portal_validation_errors": [],
            "is_valid_dynamic": False,
            "requires_human_intervention": False,
        }

    @telemetry_trace
    def select_platform(self, state: WorkflowState) -> Dict[str, Any]:
        """Select a platform that Supports the chosen workload."""
        reqs = state.get("customer_requirements", {})
        vendor_pref = reqs.get("vendor_preference")

        platforms = self.graph.filter_by_type("Platform")
        if vendor_pref:
            filtered = self.graph.filter_by_metadata({"vendor": vendor_pref})
            platforms = list(set(platforms).intersection(set(filtered)))

        selected_platform = platforms[0] if platforms else "unknown-platform"

        return {"selected_platform": selected_platform}

    @telemetry_trace
    def draft_bom(self, state: WorkflowState) -> Dict[str, Any]:
        """Draft a Bill of Materials based on platform compatibility using LLM and constraints."""
        platform_id = state.get("selected_platform")
        reqs = state.get("customer_requirements", {})
        val_errors = state.get("validation_errors", [])

        requirements = []
        for r_data in reqs.get("parsed", []):
            requirements.append(CustomerRequirement(**r_data))

        cust_req = CustomerRequest(
            request_id=reqs.get("request_id", "req-1"),
            target_platform=platform_id,
            vendor_preference=reqs.get("vendor_preference"),
            workloads=[state.get("target_workload")]
            if state.get("target_workload") != "Unknown"
            else [],
            requirements=requirements,
            previous_errors=val_errors,
        )

        candidates = self.generator.generate(cust_req)

        current_bom = []
        ranked_solutions = []
        if candidates:
            current_bom = candidates[0].components
            ranked_solutions = [c.model_dump() for c in candidates]

        attempt_count = state.get("attempt_count", 0) + 1

        return {
            "current_bom": current_bom,
            "ranked_solutions": ranked_solutions,
            "attempt_count": attempt_count,
            "max_attempts": state.get("max_attempts", 3)
        }

    @telemetry_trace
    def validate_bom(self, state: WorkflowState) -> Dict[str, Any]:
        """Deterministically validate the drafted BOM using the static RuleEngine."""
        platform_id = state.get("selected_platform")
        current_bom = state.get("current_bom", [])

        if not platform_id:
            return {
                "is_valid_static": False,
                "validation_errors": ["Missing platform."],
            }

        is_valid, _, errors = self.rule_engine.evaluate_solution(
            platform_id, current_bom
        )

        return {"is_valid_static": is_valid, "validation_errors": errors}

    @telemetry_trace
    def live_portal_validation(self, state: WorkflowState) -> Dict[str, Any]:
        """[PLACEHOLDER] - Future dynamic validation against Vendor/Partner Portals."""
        # For headless testing and current offline implementation, always return True
        return {
            "is_valid_dynamic": True,
            "requires_human_intervention": False,
            "portal_validation_errors": []
        }

    @telemetry_trace
    def update_knowledge_base(self, state: WorkflowState) -> Dict[str, Any]:
        """[PLACEHOLDER] - Future Knowledge Update Loop."""
        # IMPORTANT: Increment attempt_count to avoid infinite loop between validate_bom and update_knowledge_base
        current_attempts = state.get("attempt_count", 0)
        logger.info(f"Triggering knowledge base update loop for attempt {current_attempts + 1}")
        return {"attempt_count": current_attempts + 1}

    @telemetry_trace
    def human_intervention(self, state: WorkflowState) -> Dict[str, Any]:
        """[PLACEHOLDER] - Future Human-In-The-Loop (HITL) step."""
        return {"requires_human_intervention": False}

    @telemetry_trace
    def rank_solutions(self, state: WorkflowState) -> Dict[str, Any]:
        """Traverse HasSKU edges and rank solutions based on business logic and track deltas."""
        ranked = state.get("ranked_solutions", [])
        if not ranked:
            ranked = [{"rank": 1, "skus": [], "score": 95}]
            
        # Delta Tracking Logic
        # Calculate exactly what was added, removed, or updated from original requirements
        reqs = state.get("customer_requirements", {})
        original_reqs = reqs.get("parsed", [])
        original_skus = set()
        for r in original_reqs:
            if r.get("name", "").upper() in ("SKU", "COMPONENT"):
                original_skus.add(str(r.get("value", "")).upper())
                
        for solution in ranked:
            final_components = set(str(c).upper() for c in solution.get("components", []))
            added = list(final_components - original_skus)
            removed = list(original_skus - final_components)
            solution["delta"] = {
                "added": added,
                "removed": removed,
                "updated": len(added) + len(removed) > 0
            }

        return {"ranked_solutions": ranked}

