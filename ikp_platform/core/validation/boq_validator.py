import difflib
import logging
from typing import List, Dict, Tuple
from .validator import VendorValidator, ValidationResult, ValidationMessage
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import EngineeringObjectType

logger = logging.getLogger("ikp.validation.boq")

class BOQValidator(VendorValidator):
    """
    Validates a Bill of Quantities against the canonical catalog,
    using fuzzy matching to auto-correct minor typos.
    """

    def __init__(self, graph: GraphBuilder):
        self.graph = graph

    def fuzzy_match_sku(self, requested_sku: str, threshold: float = 0.9) -> Tuple[str, bool]:
        """
        Attempts to match a requested SKU against catalog SKUs.
        Returns (matched_sku, was_fuzzy_matched)
        """
        # Get all valid SKUs
        valid_skus = []
        for node_id, data in self.graph.graph.nodes(data=True):
            if data.get("type") in (EngineeringObjectType.SKU.value, EngineeringObjectType.COMPONENT.value):
                # Fallback to node_id tail if part_number isn't set
                part_no = data.get("attr_part_number") or node_id.split('/')[-1].upper()
                valid_skus.append((part_no, node_id))
        
        # Exact match
        for part_no, node_id in valid_skus:
            if part_no.lower() == requested_sku.lower():
                return node_id, False
                
        # Fuzzy match
        part_nos = [p[0] for p in valid_skus if p[0]]
        matches = difflib.get_close_matches(requested_sku.upper(), part_nos, n=1, cutoff=threshold)
        
        if matches:
            best_match = matches[0]
            for part_no, node_id in valid_skus:
                if part_no == best_match:
                    return node_id, True
                    
        return requested_sku, False

    def validate(self, solution_components: List[str], context: dict) -> ValidationResult:
        result = ValidationResult(
            solution_id=context.get("solution_id", "unknown"),
            validator_name="BOQFuzzyValidator",
            is_valid=True
        )
        
        corrected_components = []
        for requested_sku in solution_components:
            matched_id, was_fuzzy = self.fuzzy_match_sku(requested_sku)
            corrected_components.append(matched_id)
            
            if was_fuzzy:
                result.messages.append(ValidationMessage(
                    severity="Info",
                    message=f"Auto-corrected requested SKU '{requested_sku}' to '{matched_id}'",
                    affected_object=matched_id
                ))
            elif matched_id == requested_sku and matched_id not in self.graph.graph:
                result.messages.append(ValidationMessage(
                    severity="Error",
                    message=f"Invalid SKU requested: '{requested_sku}'. Could not find a match.",
                ))
                result.is_valid = False
                
        return result
