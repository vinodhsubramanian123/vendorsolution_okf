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
            "validation_failures": [],
            "excluded_component_ids": [],
            "tried_candidate_indices": [0],
            "needs_regeneration": False,
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
            excluded_component_ids=state.get("excluded_component_ids", []),
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
            "max_attempts": state.get("max_attempts", 3),
            "tried_candidate_indices": [0],
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

        is_valid, _, failures = self.rule_engine.evaluate_solution(
            platform_id, current_bom
        )
        
        errors = [f.message if hasattr(f, "message") else str(f) for f in failures]
        
        if is_valid:
            logger.info(f"BOM Validation passed perfectly for {platform_id} with {len(current_bom)} components.")
        else:
            logger.warning(f"BOM Validation failed with {len(errors)} errors: {errors}")

        # Store failures as dicts for state serialization
        serialized_failures = [f.model_dump() if hasattr(f, "model_dump") else {"message": str(f)} for f in failures]
        
        # Cycle Detection
        import hashlib
        bom_str = ",".join(sorted([str(c) for c in current_bom]))
        bom_hash = hashlib.sha256(bom_str.encode()).hexdigest()
        
        visited = state.get("visited_bom_hashes", [])
        cycle_detected = state.get("cycle_detected", False)
        
        if bom_hash in visited and not is_valid:
            logger.error(f"CYCLE DETECTED! BOM hash {bom_hash} has been evaluated before and failed.")
            cycle_detected = True
        elif not is_valid:
            visited.append(bom_hash)

        return {
            "is_valid_static": is_valid, 
            "validation_errors": errors,
            "validation_failures": serialized_failures,
            "visited_bom_hashes": visited,
            "cycle_detected": cycle_detected
        }

    @telemetry_trace
    def select_recovery_strategy(self, state: WorkflowState) -> Dict[str, Any]:
        """
        Dynamically recover from validation failures.
        1. Try next candidate in ranked_solutions
        2. Find substitute (Replaces / Compatible With)
        3. Drop optional component
        4. Regenerate excluding failed component
        """
        platform_id = state.get("selected_platform")
        failures = state.get("validation_failures", [])
        ranked_solutions = state.get("ranked_solutions", [])
        tried_indices = state.get("tried_candidate_indices", [0])
        excluded_ids = state.get("excluded_component_ids", [])
        current_bom = list(state.get("current_bom", []))
        
        if not failures:
            return {}
            
        failure = failures[0]
        failure_type = failure.get("failure_type") if isinstance(failure, dict) else getattr(failure, "failure_type", None)
        failed_obj = failure.get("object_id") if isinstance(failure, dict) else getattr(failure, "object_id", None)
        if not failed_obj:
            failed_obj = failure.get("category") if isinstance(failure, dict) else getattr(failure, "category", None)
        
        # 0. Missing requirements means we need to regenerate to fill gaps
        if failure_type == "missing_required_category" or (hasattr(failure_type, "value") and failure_type.value == "missing_required_category"):
            logger.info("Recovery: Missing required categories. Forcing regeneration.")
            audit_trail = state.get("recovery_audit_trail", []) + [{"action": "regenerate_missing_dependencies"}]
            return {"needs_regeneration": True, "recovery_audit_trail": audit_trail}
        
        # 1. Try next candidate
        next_idx = len(tried_indices)
        if next_idx < len(ranked_solutions):
            logger.info(f"Recovery: Trying alternative candidate profile '{ranked_solutions[next_idx].get('profile', 'Unknown')}'")
            audit_trail = state.get("recovery_audit_trail", []) + [{"action": "switch_candidate", "target": ranked_solutions[next_idx].get("profile", "Unknown")}]
            return {
                "current_bom": ranked_solutions[next_idx].get("components", []),
                "tried_candidate_indices": tried_indices + [next_idx],
                "requires_human_intervention": True, # User guidance: discuss with human due to fallback trust
                "needs_regeneration": False,
                "recovery_audit_trail": audit_trail
            }
            
        # 2. Find substitute
        if failed_obj and failed_obj in self.graph.graph:
            candidates = self.graph.get_related(failed_obj, "Replaces")
            candidates.extend(self.graph.get_related(failed_obj, "Compatible With"))
            
            for cand_id in candidates:
                if platform_id in self.graph.get_compatible(cand_id):
                    logger.info(f"Recovery: Swapping {failed_obj} for substitute {cand_id}")
                    new_bom = [c if c != failed_obj else cand_id for c in current_bom]
                    audit_trail = state.get("recovery_audit_trail", []) + [{"action": "substitute", "original": failed_obj, "new": cand_id}]
                    return {"current_bom": new_bom, "needs_regeneration": False, "recovery_audit_trail": audit_trail}
                    
        # 3. Drop optional
        if failed_obj and failed_obj in self.graph.graph:
            node = self.graph.graph.nodes[failed_obj]
            is_required = node.get("attr_is_required", True)
            
            if not is_required:
                logger.info(f"Recovery: Dropping optional component {failed_obj}")
                new_bom = [c for c in current_bom if c != failed_obj]
                audit_trail = state.get("recovery_audit_trail", []) + [{"action": "drop", "target": failed_obj}]
                return {"current_bom": new_bom, "needs_regeneration": False, "recovery_audit_trail": audit_trail}
                
        # 4. Regenerate without component
        if failed_obj:
            logger.info(f"Recovery: Regenerating BOM without {failed_obj}")
            if failed_obj not in excluded_ids:
                excluded_ids.append(failed_obj)
            audit_trail = state.get("recovery_audit_trail", []) + [{"action": "exclude_and_regenerate", "target": failed_obj}]
            return {"excluded_component_ids": excluded_ids, "needs_regeneration": True, "recovery_audit_trail": audit_trail}
            
        return {}

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
        """Aggregate validation errors and portal rejections into a full-solution FailureReport for HITL review."""
        logger.warning("Automated recovery exhausted or portal rejected solution. Escaping to HITL.")
        
        failure_report = {
            "customer_intent": state.get("customer_requirements", {}).get("raw_text", ""),
            "attempted_platform": state.get("selected_platform"),
            "excluded_components": state.get("excluded_component_ids", []),
            "internal_rule_failures": state.get("validation_failures", []),
            "holistic_portal_errors": state.get("portal_validation_errors", []),
            "recovery_audit_trail": state.get("recovery_audit_trail", []),
            "current_bom": state.get("current_bom", []),
            "cycle_detected": state.get("cycle_detected", False),
        }

        return {
            "requires_human_intervention": True,
            "human_review_payload": failure_report,
        }

    @telemetry_trace
    def rank_solutions(self, state: WorkflowState) -> Dict[str, Any]:
        """Traverse HasSKU edges and rank solutions based on business logic and track deltas."""
        ranked: List[Dict[str, Any]] = state.get("ranked_solutions", [])
        if not ranked:
            dummy: Dict[str, Any] = {"rank": 1, "skus": [], "score": 95}
            ranked = [dummy]
            
        # Delta Tracking Logic
        # Calculate exactly what was added, removed, or updated from original requirements
        reqs = state.get("customer_requirements", {})
        original_reqs = reqs.get("parsed", [])
        original_skus = set()
        logger.error(f"DEBUG: reqs={reqs}")
        for r in original_reqs:
            if r.get("name", "").upper() in ("SKU", "COMPONENT"):
                original_skus.add(str(r.get("value", "")).upper())
        logger.error(f"DEBUG: original_skus={original_skus}")
                
        for solution in ranked:
            final_components = set(str(c).upper() for c in solution.get("components", []))
            added = list(final_components - original_skus)
            removed = list(original_skus - final_components)
            solution["delta"] = {
                "added": added,
                "removed": removed,
                "updated": len(added) + len(removed) > 0
            }
            logger.info(f"Solution Profile '{solution.get('profile')}' Delta: Added {len(added)} components, Removed {len(removed)} components")

        return {"ranked_solutions": ranked}

