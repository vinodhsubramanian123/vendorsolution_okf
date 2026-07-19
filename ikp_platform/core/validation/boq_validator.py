import difflib
import logging
from typing import List, Tuple
from .validator import VendorValidator, ValidationResult, ValidationMessage
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import EngineeringObjectType

logger = logging.getLogger("ikp.validation.boq")


class BOQValidator(VendorValidator):
    """
    Validates a Bill of Quantities against the canonical catalog,
    using fuzzy matching to auto-correct minor typos.
    """

    def __init__(self, graph: GraphBuilder, vector_store=None):
        self.graph = graph
        self.vector_store = vector_store

    def fuzzy_match_sku(
        self, requested_sku: str, threshold: float = 0.9
    ) -> Tuple[str, bool, float, str]:
        """
        Attempts to match a requested SKU against catalog SKUs.
        Returns (matched_sku, was_fuzzy_matched, confidence, algorithm)
        """
        # Get all valid SKUs
        valid_skus = []
        for node_id, data in self.graph.graph.nodes(data=True):
            if data.get("type") in (
                EngineeringObjectType.SKU.value,
                EngineeringObjectType.COMPONENT.value,
            ):
                # Fallback to node_id tail if part_number isn't set
                part_no = data.get("attr_part_number") or node_id.split("/")[-1].upper()
                valid_skus.append((part_no, node_id))

        # Exact match
        for part_no, node_id in valid_skus:
            if part_no.lower() == requested_sku.lower():
                return node_id, False, 1.0, "exact"

            aliases = self.graph.graph.nodes[node_id].get("aliases", [])
            for alias in aliases:
                if alias.lower() == requested_sku.lower():
                    return node_id, False, 1.0, "alias_exact"

        # Fuzzy match (string similarity)
        part_nos = [p[0] for p in valid_skus if p[0]]
        matches = difflib.get_close_matches(
            requested_sku.upper(), part_nos, n=1, cutoff=threshold
        )

        if matches:
            best_match = matches[0]
            score = difflib.SequenceMatcher(
                None, requested_sku.upper(), best_match
            ).ratio()
            for part_no, node_id in valid_skus:
                if part_no == best_match:
                    return node_id, True, score, "difflib"

        # Semantic fallback
        if self.vector_store:
            results = self.vector_store.semantic_search(requested_sku, n_results=5)
            # Dynamic threshold based on length (shorter strings need lower threshold)
            threshold_score = 0.55 if len(requested_sku) <= 10 else 0.80

            for res_id, score in results:
                if res_id in self.graph.graph:
                    node_type = self.graph.graph.nodes[res_id].get("type")
                    if node_type in (
                        EngineeringObjectType.SKU.value,
                        EngineeringObjectType.COMPONENT.value,
                    ):
                        # Accept semantic matches based on dynamic threshold
                        if score >= threshold_score:
                            logger.info(
                                f"Semantic fallback match: '{requested_sku}' -> '{res_id}' (score: {score:.2f} >= {threshold_score})"
                            )
                            return res_id, True, score, "semantic"

        return requested_sku, False, 0.0, "none"

    def _check_completeness(self, component_ids: List[str], result: ValidationResult):
        categories_found = set()
        for comp_id in component_ids:
            if comp_id in self.graph.graph:
                node = self.graph.graph.nodes[comp_id]
                node_type = node.get("type")
                if node_type == EngineeringObjectType.PLATFORM.value:
                    categories_found.add("Platform")
                else:
                    cat = node.get("attr_component_category") or node.get("category")
                    if cat:
                        categories_found.add(cat.upper())

        # Determine mandatory categories dynamically from the platform node
        platform_id = None
        for comp_id in component_ids:
            if comp_id in self.graph.graph and self.graph.graph.nodes[comp_id].get("type") == EngineeringObjectType.PLATFORM.value:
                platform_id = comp_id
                break

        mandatory = ["PLATFORM"] # Always need a platform at minimum
        if platform_id:
            plat_data = self.graph.graph.nodes[platform_id]
            mandatory.extend(plat_data.get("mandatory_categories", []))
        else:
            # If no platform was found, we can't determine mandatory categories,
            # but the lack of a platform will be flagged.
            pass

        missing = []
        for req in mandatory:
            if req.upper() not in categories_found:
                missing.append(req)

        if missing:
            result.messages.append(
                ValidationMessage(
                    severity="Warning",
                    message=f"BOQ may be incomplete. Missing core categories: {', '.join(missing)}",
                )
            )

    def validate(
        self, solution_components: List[str], context: dict
    ) -> ValidationResult:
        result = ValidationResult(
            solution_id=context.get("solution_id", "unknown"),
            validator_name="BOQFuzzyValidator",
            is_valid=True,
        )

        corrected_components = []
        for requested_sku in solution_components:
            matched_id, was_fuzzy, score, algo = self.fuzzy_match_sku(requested_sku)
            corrected_components.append(matched_id)

            if was_fuzzy:
                result.messages.append(
                    ValidationMessage(
                        severity="Info",
                        message=f"Auto-corrected requested SKU '{requested_sku}' to '{matched_id}' (algo: {algo}, confidence: {score:.2f})",
                        affected_object=matched_id,
                    )
                )
            elif matched_id == requested_sku and matched_id not in self.graph.graph:
                result.messages.append(
                    ValidationMessage(
                        severity="Error",
                        message=f"Invalid SKU requested: '{requested_sku}'. Could not find a match.",
                    )
                )
                result.is_valid = False

        self._check_completeness(corrected_components, result)
        return result
