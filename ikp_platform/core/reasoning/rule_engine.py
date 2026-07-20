"""
Rule Engine — Deterministic constraint and compatibility evaluation.

Governs: Blueprint 05 §8-§11 (Engineering Reasoning)

Traverses the graph to evaluate capabilities, dependencies, constraints, and rules.
Generates an explainable reasoning chain.
"""

import logging
from typing import List, Tuple, Dict

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import RuleSeverity, EngineeringObjectType, ValidationFailure, ValidationFailureType
from ikp_platform.core.reasoning.remediation_engine import RemediationEngine
from ikp_platform.core.validation.pipeline import ValidationStep, ValidationContext

logger = logging.getLogger("ikp.reasoning.rule_engine")


class RuleEngine(ValidationStep):
    """
    Evaluates business rules, constraints, and dependencies against a proposed configuration.
    """

    def __init__(self, graph: GraphBuilder):
        self.graph = graph

    def evaluate_solution(
        self, platform_id: str, component_ids: List[str]
    ) -> Tuple[bool, List[str], List[ValidationFailure]]:
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
            return (
                False,
                reasoning_chain,
                [ValidationFailure(
                    failure_type=ValidationFailureType.INVALID_SKU,
                    object_id=platform_id,
                    message=f"Platform {platform_id} not found in repository",
                    payload={"invalid_skus": [platform_id]}
                )],
            )

        all_components = [platform_id] + component_ids

        # 1. Check compatibility
        compat_errors = self._check_compatibility(
            platform_id, component_ids, reasoning_chain
        )
        errors.extend(compat_errors)

        # 2. Check constraints
        constraint_errors = self._evaluate_constraints(
            platform_id, component_ids, reasoning_chain
        )
        errors.extend(constraint_errors)

        # 3. Check dependencies
        dep_errors = self._check_dependencies(all_components, reasoning_chain)
        errors.extend(dep_errors)

        # 4. Evaluate rules
        rule_errors = self._evaluate_rules(all_components, reasoning_chain)
        errors.extend(rule_errors)

        if errors:
            is_valid = False
            msg = f"Evaluation failed with {len(errors)} errors."
            reasoning_chain.append(msg)
            logger.warning(msg)
            for err in errors:
                logger.warning(f"  - {err.message}")
        else:
            msg = "Evaluation successful. All constraints and rules satisfied."
            reasoning_chain.append(msg)
            logger.info(msg)

        return is_valid, reasoning_chain, errors

    def execute(self, context: ValidationContext) -> ValidationContext:
        is_valid, reasoning, errors = self.evaluate_solution(
            context.platform_id or "",
            context.corrected_components or context.original_components
        )
        
        context.is_valid = context.is_valid and is_valid
        context.reasoning_chain.extend(reasoning)
        context.errors.extend(errors)
        
        if hasattr(self, "_temp_pass_rules"):
            if "passed_rules" not in context.metadata:
                context.metadata["passed_rules"] = []
            context.metadata["passed_rules"].extend(self._temp_pass_rules)
            self._temp_pass_rules = []
            
        return context

    def _check_compatibility(
        self, platform_id: str, component_ids: List[str], reasoning_chain: List[str]
    ) -> List[ValidationFailure]:
        """Check if all components are compatible with the platform, enforcing STRICT Solution Domain isolation."""
        errors = []
        platform_compatible = set(self.graph.get_compatible(platform_id))

        platform_data = self.graph.graph.nodes[platform_id]
        platform_domain = str(platform_data.get("solution_domain") or "Unknown").lower()

        for comp_id in component_ids:
            if comp_id not in self.graph.graph:
                errors.append(ValidationFailure(
                    failure_type=ValidationFailureType.INVALID_SKU,
                    object_id=comp_id,
                    message=f"Component not found: {comp_id}",
                    payload={"invalid_skus": [comp_id]}
                ))
                continue

            comp_data = self.graph.graph.nodes[comp_id]
            comp_domain = str(comp_data.get("solution_domain") or "Unknown").lower()

            # Determine explicit compatibility between component and platform
            is_explicitly_compatible = comp_id in platform_compatible
            if not is_explicitly_compatible:
                comp_outbound = set(self.graph.get_compatible(comp_id))
                if platform_id in comp_outbound:
                    is_explicitly_compatible = True
                else:
                    contains_targets = self.graph.get_related(platform_id, "Contains")
                    if comp_id in contains_targets:
                        is_explicitly_compatible = True

            # --- STRICT DOMAIN ISOLATION BARRIER ---
            # Reject cross-domain selections UNLESS they are explicitly linked via a compatibility edge
            if comp_domain != platform_domain and comp_domain != "unknown":
                if not is_explicitly_compatible:
                    err_msg = f"CROSS-DOMAIN BLEED DETECTED: Rejected {comp_id} (Domain: {comp_domain}) on Platform {platform_id} (Domain: {platform_domain}) due to missing explicit compatibility edge."
                    errors.append(ValidationFailure(
                        failure_type=ValidationFailureType.INCOMPATIBLE,
                        object_id=comp_id,
                        message=err_msg,
                        payload={"incompatible": [comp_id], "domain_conflict": True}
                    ))
                    logger.error(err_msg)
                    continue

            if not is_explicitly_compatible:
                msg = f"Warning: {comp_id} has no explicit compatibility link to {platform_id}"
                reasoning_chain.append(msg)
                logger.warning(msg)
            else:
                msg = f"Validated compatibility: {comp_id} <-> {platform_id}"
                reasoning_chain.append(msg)
                logger.debug(msg)
                
            # Check for mutual exclusions among components in the BOQ
            for other_id in component_ids:
                if comp_id != other_id and other_id in self.graph.graph:
                    incompatible = False
                    # Check edges in both directions
                    if self.graph.graph.has_edge(comp_id, other_id) and self.graph.graph[comp_id][other_id].get("relationship_type") == "Incompatible With":
                        incompatible = True
                    if self.graph.graph.has_edge(other_id, comp_id) and self.graph.graph[other_id][comp_id].get("relationship_type") == "Incompatible With":
                        incompatible = True
                        
                    if incompatible:
                        err_msg = f"{comp_id} is incompatible with {other_id}"
                        # avoid duplicate errors for the same pair
                        if not any(e.message == err_msg for e in errors) and not any(e.message == f"{other_id} is incompatible with {comp_id}" for e in errors):
                            errors.append(ValidationFailure(
                                failure_type=ValidationFailureType.INCOMPATIBLE,
                                object_id=comp_id,
                                message=err_msg,
                                payload={"incompatible_pair": [comp_id, other_id]}
                            ))
                            logger.error(err_msg)

        return errors

    def _evaluate_constraints(
        self, platform_id: str, component_ids: List[str], reasoning_chain: List[str]
    ) -> List[ValidationFailure]:
        """Evaluate platform constraints (e.g., max memory, max drives, category limits)."""
        errors: List[ValidationFailure] = []

        # Get all constraints attached to the platform
        platform_constraints = set()
        for other_id in self.graph.get_related(platform_id, "Contains"):
            if self.graph.graph.nodes[other_id].get("type") in (
                EngineeringObjectType.CONSTRAINT.value,
                EngineeringObjectType.CATEGORY_LIMIT.value,
            ):
                platform_constraints.add(other_id)


        if not platform_constraints:
            reasoning_chain.append("No explicit constraints found for platform.")
            return errors

        reasoning_chain.append(
            f"Evaluating {len(platform_constraints)} platform constraints..."
        )

        # Aggregate components by type and subcategory for limit checking
        comp_categories: Dict[str, int] = {}
        comp_subcategories: Dict[str, int] = {}
        # Evaluate static constraints and limits...
        # We will also evaluate mathematical dynamic resource consumption.
        provided_resources = {"pcie_slots": 0.0} # Base platform often provides some, but let's calculate from components.
        consumed_resources: Dict[str, float] = {}

        for comp_id in component_ids:
            if comp_id not in self.graph.graph: continue
            data = self.graph.graph.nodes[comp_id]
            provided = data.get("provided_resources", {})
            consumed = data.get("consumed_resources", {})
            
            for res, val in provided.items():
                provided_resources[res] = provided_resources.get(res, 0.0) + val
            for res, val in consumed.items():
                consumed_resources[res] = consumed_resources.get(res, 0.0) + val

        # Calculate Absolute Maximum Theoretical Capacity for resources consumed
        max_theoretical_resources = {}
        for res in consumed_resources.keys():
            # Base provided by the platform itself (not the current BOM)
            platform_node = self.graph.graph.nodes[platform_id] if platform_id in self.graph.graph else {}
            max_res = platform_node.get("provided_resources", {}).get(res, 0.0)
            
            # Check all category limits for providers
            for constraint_id in platform_constraints:
                c_data = self.graph.graph.nodes[constraint_id]
                if c_data.get("type") == EngineeringObjectType.CATEGORY_LIMIT.value:
                    limit_val = c_data.get("limit_value")
                    target_subcat = c_data.get("attr_target_subcategory")
                    target_cat = c_data.get("attr_target_category")
                    
                    if isinstance(limit_val, int) and limit_val > 0 and (target_subcat or target_cat):
                        # Find max provision rate among compatible components for this category
                        max_provider_rate = 0.0
                        for comp_id in self.graph.get_related(platform_id, "Compatible With"):
                            if comp_id in self.graph.graph:
                                node = self.graph.graph.nodes[comp_id]
                                n_cat = node.get("attr_component_category")
                                n_subcat = node.get("attr_component_subcategory")
                                if (target_subcat and n_subcat == target_subcat) or (target_cat and n_cat == target_cat):
                                    prov = node.get("provided_resources", {}).get(res, 0.0)
                                    if prov > max_provider_rate:
                                        max_provider_rate = prov
                        
                        if max_provider_rate > 0:
                            max_res += max_provider_rate * limit_val
                            
            max_theoretical_resources[res] = max_res

        for res, consumed_val in consumed_resources.items():
            provided_val = provided_resources.get(res, 0.0)
            max_theoretical = max_theoretical_resources.get(res, 0.0)
            if consumed_val > provided_val:
                msg = f"Resource Exhausted: Solution requires {consumed_val} {res}, but only {provided_val} {res} are currently provided. (Absolute Maximum Theoretical Capacity: {max_theoretical} {res})"
                errors.append(ValidationFailure(
                    failure_type=ValidationFailureType.CATEGORY_LIMIT_EXCEEDED,
                    object_id=platform_id,
                    message=msg,
                    payload={"resource": res, "consumed": consumed_val, "provided": provided_val}
                ))
                reasoning_chain.append(f"Failed Math Validation: {msg}")
                logger.error(msg)
            else:
                reasoning_chain.append(f"Math Validation Passed: {consumed_val}/{provided_val} {res} utilized.")

        for comp_id in component_ids:
            if comp_id in self.graph.graph:
                node = self.graph.graph.nodes[comp_id]
                cat = node.get("attr_component_category", "Unknown")
                subcat = node.get("attr_component_subcategory") or "Unknown"

                # Check for packages
                inclusive_qty = node.get("attr_inclusive_qty") or 1

                comp_categories[cat] = comp_categories.get(cat, 0) + inclusive_qty
                if subcat != "Unknown":
                    comp_subcategories[subcat] = (
                        comp_subcategories.get(subcat, 0) + inclusive_qty
                    )

        # Evaluate each constraint
        for constraint_id in platform_constraints:
            c_data = self.graph.graph.nodes[constraint_id]
            limit_name = c_data.get("limit_name", "").lower()
            limit_value = c_data.get("limit_value")
            c_type = c_data.get("type")

            if c_type == EngineeringObjectType.CATEGORY_LIMIT.value:
                target_subcat = c_data.get("attr_target_subcategory")
                target_cat = c_data.get("attr_target_category")

                current_qty = 0
                if target_subcat and target_subcat in comp_subcategories:
                    current_qty = comp_subcategories[target_subcat]
                elif target_cat and target_cat in comp_categories:
                    current_qty = comp_categories[target_cat]

                min_qty = c_data.get("min_qty")
                if (target_subcat or target_cat):
                    if isinstance(limit_value, int) and current_qty > limit_value:
                        errors.append(ValidationFailure(
                            failure_type=ValidationFailureType.CATEGORY_LIMIT_EXCEEDED,
                            rule_id=constraint_id,
                            category=target_cat or target_subcat,
                            message=f"Constraint violation: {limit_name} (Max: {limit_value}, Requested: {current_qty})",
                            payload={"limit_exceeded": {"category": target_cat or target_subcat, "limit": limit_value, "requested": current_qty}}
                        ))
                    elif isinstance(min_qty, int) and current_qty < min_qty:
                        errors.append(ValidationFailure(
                            failure_type=ValidationFailureType.MISSING_REQUIRED_CATEGORY,
                            rule_id=constraint_id,
                            category=target_cat or target_subcat,
                            message=f"Constraint violation: {limit_name} (Min: {min_qty}, Requested: {current_qty})",
                            payload={"missing": [target_cat or target_subcat]}
                        ))
                    else:
                        evidence = (
                            c_data.get("evidence", [{}])[0]
                            if c_data.get("evidence")
                            else {}
                        )
                        conf_raw = evidence.get("confidence", "UNKNOWN")
                        conf = (
                            conf_raw.value
                            if hasattr(conf_raw, "value")
                            else str(conf_raw)
                        )
                        snippet = str(
                            evidence.get("original_text_snippet") or ""
                        ).strip()[:120]
                        reasoning_chain.append(
                            f"Constraint passed: {c_data.get('title')} ({current_qty} <= {limit_value}) [Confidence: {conf}] | Trace: '{snippet}'"
                        )
            elif c_type == EngineeringObjectType.CONSTRAINT.value:
                # Generic constraints require a CSP solver for thermal/power/spatial properties.
                # Here we log them as unevaluated, relying on CategoryLimits for component counts.
                reasoning_chain.append(
                    f"Generic constraint noted (requires CSP solver): {c_data.get('title')}"
                )

        return errors

    def _check_dependencies(
        self, component_ids: List[str], reasoning_chain: List[str]
    ) -> List[ValidationFailure]:
        """Check if all required dependencies are present in the solution."""
        errors = []
        comp_set = set(component_ids)

        for comp_id in component_ids:
            deps = self.graph.get_dependencies(comp_id)
            for dep_id in deps:
                if dep_id not in comp_set:
                    errors.append(ValidationFailure(
                        failure_type=ValidationFailureType.MISSING_REQUIRED_CATEGORY,
                        object_id=comp_id,
                        message=f"Missing dependency: {comp_id} requires {dep_id}",
                        payload={"missing": [dep_id]}
                    ))
                else:
                    reasoning_chain.append(
                        f"Dependency satisfied: {comp_id} -> {dep_id}"
                    )

        return errors

    def _evaluate_rules(
        self, component_ids: List[str], reasoning_chain: List[str]
    ) -> List[ValidationFailure]:
        """Evaluate applicable engineering rules."""
        errors = []

        # In a full implementation, we would parse trigger conditions using a parser
        # For V1, we log the applicable rules
        all_rules = self.graph.filter_by_type(EngineeringObjectType.RULE.value)
        applicable_count = 0

        for rule_id in all_rules:
            r_data = self.graph.graph.nodes[rule_id]
            applicable_objects = set(r_data.get("applicable_objects", []))

            # Check if any applicable object matches component ID exactly or as a URI suffix
            applies = False
            matched_comp_id = None
            for app_obj in applicable_objects:
                app_obj_clean = app_obj.lower().strip()
                for comp_id in component_ids:
                    comp_id_clean = comp_id.lower().strip()
                    if comp_id_clean == app_obj_clean or comp_id_clean.endswith(
                        f"/{app_obj_clean}"
                    ):
                        applies = True
                        matched_comp_id = comp_id
                        break
                if applies:
                    break

            if applies:
                applicable_count += 1
                severity_raw = (
                    r_data.get("severity")
                    or r_data.get("attr_severity")
                    or RuleSeverity.INFO.value
                )
                severity = (
                    severity_raw.value
                    if hasattr(severity_raw, "value")
                    else str(severity_raw)
                )

                evidence = (
                    r_data.get("evidence", [{}])[0] if r_data.get("evidence") else {}
                )
                conf_raw = evidence.get("confidence", "UNKNOWN")
                conf = conf_raw.value if hasattr(conf_raw, "value") else str(conf_raw)
                snippet = str(evidence.get("original_text_snippet") or "").strip()[:120]
                rule_text = (
                    r_data.get("description")
                    or r_data.get("attr_expected_outcome")
                    or r_data.get("title")
                )

                triggers = r_data.get("trigger_conditions", [])
                targets = r_data.get("dependency_targets", [])
                negated = r_data.get("negated", False)

                if not triggers and not targets:
                    msg = f"Rule noted for manual review (unparsed schema): {rule_text} [{severity}]"
                    reasoning_chain.append(msg)
                    continue

                violation = False
                is_requires = any("requires" in str(t).lower() or "requires" == str(t).upper() for t in triggers)
                is_incompatible = any("incompatible" in str(t).lower() or "incompatible_with" == str(t).upper() for t in triggers)

                if is_requires:
                    for target in targets:
                        target_clean = target.lower().strip()
                        target_found = any(
                            c.lower().strip() == target_clean or c.lower().strip().endswith(f"/{target_clean}")
                            for c in component_ids
                        )
                        if not target_found and not negated:
                            violation = True
                            break
                        elif target_found and negated:
                            violation = True
                            break
                elif is_incompatible:
                    for target in targets:
                        target_clean = target.lower().strip()
                        target_found = any(
                            c.lower().strip() == target_clean or c.lower().strip().endswith(f"/{target_clean}")
                            for c in component_ids
                        )
                        if target_found and not negated:
                            violation = True
                            break
                        elif not target_found and negated:
                            violation = True
                            break
                else:
                    msg = f"Rule noted for manual review (unrecognized triggers): {rule_text} [{severity}]"
                    reasoning_chain.append(msg)
                    continue

                category = "General"
                subcategory = "General"
                if matched_comp_id and matched_comp_id in self.graph.graph:
                    c_data = self.graph.graph.nodes[matched_comp_id]
                    category = c_data.get("attr_component_category", "General")
                    subcategory = c_data.get("attr_component_subcategory", "General")

                if violation:
                    msg = f"Rule Violation: {rule_text} [{severity}] [Confidence: {conf}] | Trace: '{snippet}'"
                    reasoning_chain.append(msg)
                    if severity in (RuleSeverity.ERROR.value, RuleSeverity.CRITICAL.value):
                        errors.append(ValidationFailure(
                            failure_type=ValidationFailureType.RULE_VIOLATION,
                            rule_id=rule_id,
                            message=f"Rule Violation: {rule_text}",
                            payload={"rule_violation": rule_id, "category": category, "subcategory": subcategory}
                        ))
                else:
                    msg = f"Rule satisfied: {rule_text} [Confidence: {conf}]"
                    reasoning_chain.append(msg)
                    # Use a new context attribute to store passing validations structured
                    if not hasattr(self, "_temp_pass_rules"):
                        self._temp_pass_rules = []
                    self._temp_pass_rules.append({
                        "title": msg,
                        "category": category,
                        "subcategory": subcategory
                    })

        # Removed KPI reporting
        return errors
