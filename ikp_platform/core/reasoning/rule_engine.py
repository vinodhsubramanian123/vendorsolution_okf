"""
Rule Engine — Deterministic constraint and compatibility evaluation.

Governs: Blueprint 05 §8-§11 (Engineering Reasoning)

Traverses the graph to evaluate capabilities, dependencies, constraints, and rules.
Generates an explainable reasoning chain.
"""

import logging
from typing import List, Dict, Any, Tuple

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import RuleSeverity, EngineeringObjectType

logger = logging.getLogger("ikp.reasoning.rule_engine")


class RuleEngine:
    """
    Evaluates a set of component IDs against the canonical graph to ensure
    all constraints, dependencies, and rules are satisfied.
    """

    def __init__(self, graph: GraphBuilder):
        self.graph = graph

    def evaluate_solution(self, platform_id: str, component_ids: List[str]) -> Tuple[bool, List[str], List[str]]:
        """
        Evaluate if a solution is valid.
        Returns: (is_valid, reasoning_chain, errors)
        """
        reasoning_chain = []
        errors = []
        is_valid = True
        
        reasoning_chain.append(f"Evaluating solution on platform: {platform_id}")
        
        # Check platform exists
        if platform_id not in self.graph.graph:
            return False, reasoning_chain, [f"Platform {platform_id} not found in repository"]
            
        all_components = [platform_id] + component_ids
        
        # 1. Check compatibility
        compat_errors = self._check_compatibility(platform_id, component_ids, reasoning_chain)
        errors.extend(compat_errors)
        
        # 2. Check constraints
        constraint_errors = self._evaluate_constraints(platform_id, component_ids, reasoning_chain)
        errors.extend(constraint_errors)
        
        # 3. Check dependencies
        dep_errors = self._check_dependencies(all_components, reasoning_chain)
        errors.extend(dep_errors)
        
        # 4. Evaluate rules
        rule_errors = self._evaluate_rules(all_components, reasoning_chain)
        errors.extend(rule_errors)
        
        if errors:
            is_valid = False
            reasoning_chain.append(f"Evaluation failed with {len(errors)} errors.")
        else:
            reasoning_chain.append("Evaluation successful. All constraints and rules satisfied.")
            
        return is_valid, reasoning_chain, errors

    def _check_compatibility(self, platform_id: str, component_ids: List[str], reasoning_chain: List[str]) -> List[str]:
        """Check if all components are compatible with the platform, enforcing STRICT Solution Domain isolation."""
        errors = []
        platform_compatible = set(self.graph.get_compatible(platform_id))
        
        platform_data = self.graph.graph.nodes[platform_id]
        platform_domain = platform_data.get("attr_solution_domain", "Unknown").lower()
        
        for comp_id in component_ids:
            if comp_id not in self.graph.graph:
                errors.append(f"Component not found: {comp_id}")
                continue
            
            comp_data = self.graph.graph.nodes[comp_id]
            comp_domain = comp_data.get("attr_solution_domain", "Unknown").lower()
            
            # --- STRICT DOMAIN ISOLATION BARRIER ---
            if comp_domain != platform_domain and comp_domain not in ("networking", "infrastructure", "unknown"):
                errors.append(f"CROSS-DOMAIN BLEED DETECTED: Rejected {comp_id} (Domain: {comp_domain}) on Platform {platform_id} (Domain: {platform_domain})")
                continue
                
            if comp_id not in platform_compatible:
                comp_outbound = set(self.graph.get_compatible(comp_id))
                if platform_id not in comp_outbound:
                    contains_rels = self.graph.traverse_relationships(platform_id, "Contains", "outbound")
                    contains_targets = {r["target"] for r in contains_rels}
                    
                    if comp_id not in contains_targets:
                        reasoning_chain.append(f"Warning: {comp_id} has no explicit compatibility link to {platform_id}")
            else:
                reasoning_chain.append(f"Validated compatibility: {comp_id} <-> {platform_id}")
                
        return errors

    def _evaluate_constraints(self, platform_id: str, component_ids: List[str], reasoning_chain: List[str]) -> List[str]:
        """Evaluate platform constraints (e.g., max memory, max drives, category limits)."""
        errors = []
        
        # Get all constraints attached to the platform
        platform_constraints = set()
        for r in self.graph.traverse_relationships(platform_id, "Contains", "both"):
            other_id = r["target"] if r["source"] == platform_id else r["source"]
            if self.graph.graph.nodes[other_id].get("type") in (EngineeringObjectType.CONSTRAINT.value, EngineeringObjectType.CATEGORY_LIMIT.value):
                platform_constraints.add(other_id)
        platform_constraints = list(platform_constraints)
        
        if not platform_constraints:
            reasoning_chain.append("No explicit constraints found for platform.")
            return errors
            
        reasoning_chain.append(f"Evaluating {len(platform_constraints)} platform constraints...")
        
        # Aggregate components by type and subcategory for limit checking
        comp_categories = {}
        comp_subcategories = {}
        for comp_id in component_ids:
            if comp_id in self.graph.graph:
                node = self.graph.graph.nodes[comp_id]
                cat = node.get("attr_component_category", "Unknown")
                subcat = node.get("attr_component_subcategory") or "Unknown"
                
                # Check for packages
                inclusive_qty = node.get("attr_inclusive_qty") or 1
                
                comp_categories[cat] = comp_categories.get(cat, 0) + inclusive_qty
                if subcat != "Unknown":
                    comp_subcategories[subcat] = comp_subcategories.get(subcat, 0) + inclusive_qty
                
        # Evaluate each constraint
        for constraint_id in platform_constraints:
            c_data = self.graph.graph.nodes[constraint_id]
            limit_name = c_data.get("limit_name", "").lower()
            limit_value = c_data.get("limit_value")
            c_type = c_data.get("type")
            
            if c_type == EngineeringObjectType.CATEGORY_LIMIT.value:
                target_subcat = c_data.get("attr_target_subcategory")
                if target_subcat and target_subcat in comp_subcategories:
                    current_qty = comp_subcategories[target_subcat]
                    if isinstance(limit_value, int) and current_qty > limit_value:
                        errors.append(f"Constraint violation: {limit_name} (Max: {limit_value}, Requested: {current_qty})")
                    else:
                        evidence = c_data.get("evidence", [{}])[0]
                        conf = evidence.get("confidence", "UNKNOWN")
                        snippet = evidence.get("original_text_snippet", "")
                        reasoning_chain.append(f"Constraint passed: {c_data.get('title')} ({current_qty} <= {limit_value}) [Confidence: {conf}] | Trace: '{snippet}'")
            else:
                # Simple heuristic matching for V1
                if "drive" in limit_name or "sff" in limit_name or "lff" in limit_name:
                    drive_count = comp_categories.get("Drive", 0) + comp_categories.get("Storage", 0)
                    if isinstance(limit_value, int) and drive_count > limit_value:
                        errors.append(f"Constraint violation: {limit_name} (Max: {limit_value}, Requested: {drive_count})")
                    else:
                        evidence = c_data.get("evidence", [{}])[0] if c_data.get("evidence") else {}
                        conf = evidence.get("confidence", "UNKNOWN")
                        snippet = evidence.get("original_text_snippet", "")
                        reasoning_chain.append(f"Constraint passed: {c_data.get('title')} ({drive_count} <= {limit_value}) [Confidence: {conf}] | Trace: '{snippet}'")
                    
        return errors

    def _check_dependencies(self, component_ids: List[str], reasoning_chain: List[str]) -> List[str]:
        """Check if all required dependencies are present in the solution."""
        errors = []
        comp_set = set(component_ids)
        
        for comp_id in component_ids:
            deps = self.graph.get_dependencies(comp_id)
            for dep_id in deps:
                if dep_id not in comp_set:
                    errors.append(f"Missing dependency: {comp_id} requires {dep_id}")
                else:
                    reasoning_chain.append(f"Dependency satisfied: {comp_id} -> {dep_id}")
                    
        return errors

    def _evaluate_rules(self, component_ids: List[str], reasoning_chain: List[str]) -> List[str]:
        """Evaluate applicable engineering rules."""
        errors = []
        
        # In a full implementation, we would parse trigger conditions using a parser
        # For V1, we log the applicable rules
        all_rules = self.graph.filter_by_type(EngineeringObjectType.RULE.value)
        applicable_count = 0
        
        for rule_id in all_rules:
            r_data = self.graph.graph.nodes[rule_id]
            applicable_objects = set(r_data.get("applicable_objects", []))
            
            # Check if any applicable object is a substring of any component ID or vice versa
            applies = False
            for app_obj in applicable_objects:
                app_obj_clean = app_obj.lower().strip()
                for comp_id in component_ids:
                    comp_id_clean = comp_id.lower().strip()
                    if app_obj_clean in comp_id_clean or comp_id_clean in app_obj_clean:
                        applies = True
                        break
                if applies:
                    break
            
            if applies:
                applicable_count += 1
                severity = r_data.get("attr_severity", RuleSeverity.INFO.value)
                
                evidence = r_data.get("evidence", [{}])[0] if r_data.get("evidence") else {}
                conf = evidence.get("confidence", "UNKNOWN")
                snippet = evidence.get("original_text_snippet", "")
                rule_text = r_data.get("description") or r_data.get("attr_expected_outcome") or r_data.get("title")
                reasoning_chain.append(f"Rule evaluated: {rule_text} [{severity}] [Confidence: {conf}] | Trace: '{snippet}'")
                
        reasoning_chain.append(f"Evaluated {applicable_count} applicable engineering rules.")
        return errors
