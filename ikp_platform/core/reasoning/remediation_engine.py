import logging
from typing import List, Dict, Any
from ikp_platform.core.ontology.models import ValidationFailure, ValidationFailureType, RelationshipType
from ikp_platform.core.validation.pipeline import ValidationStep, ValidationContext
from ikp_platform.core.repository.graph_builder import GraphBuilder

logger = logging.getLogger("ikp.reasoning.remediation")

class RemediationEngine(ValidationStep):
    """
    Analyzes validation failures and generates actionable architectural remedies.
    """
    def __init__(self, graph: GraphBuilder):
        self.graph = graph

    def generate_remediations(self, platform_id: str, errors: List[ValidationFailure]) -> List[ValidationFailure]:
        for error in errors:
            if error.failure_type == ValidationFailureType.CATEGORY_LIMIT_EXCEEDED:
                self._remediate_category_limit(platform_id, error)
            elif error.failure_type == ValidationFailureType.MISSING_REQUIRED_CATEGORY:
                self._remediate_missing_category(platform_id, error)
            elif error.failure_type == ValidationFailureType.INCOMPATIBLE:
                self._remediate_incompatible(platform_id, error)
                
        return errors

    def execute(self, context: ValidationContext) -> ValidationContext:
        context.errors = self.generate_remediations(context.platform_id or "", context.errors)
        return context

    def _remediate_category_limit(self, platform_id: str, error: ValidationFailure):
        # 1. Resource Exhaustion
        if "resource" in error.payload:
            res = error.payload["resource"]
            providers = []
            for comp_id in self.graph.get_related(platform_id, "Compatible With"):
                if comp_id in self.graph.graph:
                    node = self.graph.graph.nodes[comp_id]
                    if node.get("provided_resources", {}).get(res, 0.0) > 0:
                        title = node.get("title") or comp_id
                        providers.append(title)
            
            if providers:
                # Deduplicate titles
                unique_providers = list(set(providers))
                suggestions = ", ".join(unique_providers[:3])
                if len(unique_providers) > 3:
                    suggestions += f" (and {len(unique_providers)-3} more)"
                
                error.remediations.append(f"Add a component that provides {res}, such as: {suggestions}")
                
            if "storage" in res.lower() or "bay" in res.lower():
                error.remediations.append("Alternatively, consider choosing Direct NVMe drives to bypass storage controller bay limits.")

        # 2. Static Limit Exceeded
        elif "limit_exceeded" in error.payload:
            cat = error.payload["limit_exceeded"].get("category", "")
            if cat:
                error.remediations.append(f"Remove one or more '{cat}' components from the BOQ to stay within the maximum limit.")
                if "storage" in cat.lower() or "controller" in cat.lower():
                    error.remediations.append("Consider high-density Direct NVMe options to consolidate storage without needing additional controllers.")

    def _remediate_missing_category(self, platform_id: str, error: ValidationFailure):
        missing_cats = error.payload.get("missing", [])
        for cat in missing_cats:
            options = []
            for comp_id in self.graph.get_related(platform_id, "Compatible With"):
                if comp_id in self.graph.graph:
                    node = self.graph.graph.nodes[comp_id]
                    n_cat = node.get("attr_component_category")
                    n_subcat = node.get("attr_component_subcategory")
                    if (n_cat and n_cat.lower() == cat.lower()) or (n_subcat and n_subcat.lower() == cat.lower()):
                        options.append(node.get("title") or comp_id)
            
            if options:
                unique_options = list(set(options))
                suggestions = ", ".join(unique_options[:3])
                error.remediations.append(f"Add a compatible '{cat}'. Suggested: {suggestions}")
            else:
                error.remediations.append(f"Add a compatible '{cat}' to the BOQ.")

    def _remediate_incompatible(self, platform_id: str, error: ValidationFailure):
        if "incompatible_pair" in error.payload:
            pair = error.payload["incompatible_pair"]
            error.remediations.append(f"Remove either {pair[0]} or {pair[1]} as they are mutually exclusive.")
        elif error.payload.get("domain_conflict"):
            error.remediations.append("Ensure all components belong to the same Solution Domain, or explicitly link them with a compatibility rule.")
        else:
            error.remediations.append("Remove the incompatible component from the BOQ.")
