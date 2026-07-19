"""
Intent Parser — Extracts structured engineering requirements from natural language.

Governs: Blueprint 05 §4 (Customer Requirements)

Customer requests SHALL be converted into structured engineering requirements
before reasoning begins.
"""

import logging

from ikp_platform.core.ontology.models import CustomerRequest, CustomerRequirement
from ikp_platform.core.reasoning.llm_client import LLMClient

logger = logging.getLogger("ikp.reasoning.intent_parser")


class IntentParser:
    """
    Parses unstructured customer intent into a structured CustomerRequest.
    V1.0 uses heuristic/keyword extraction. Future versions can use LLM structured outputs.
    """

    def __init__(self):
        self.llm = LLMClient()
        # V1 heuristics removed.
        # Intent parsing now relies completely on LLM structured outputs for 
        # vendor and product agnosticism.

    def parse_request(self, raw_text: str) -> CustomerRequest:
        """Parse natural language into a structured request using LLM."""
        logger.info(f"Parsing customer request: '{raw_text[:50]}...'")

        parsed = self.llm.parse_intent(raw_text)

        # Fallback if LLM failed entirely
        if not parsed.get("workloads") and not parsed.get("requirements") and not parsed.get("vendor_preference"):
            logger.warning(
                "LLM returned empty or failed. Returning raw text as unstructured requirement."
            )
            request = CustomerRequest(
                raw_text=raw_text,
                requirements=[],
                workloads=[],
            )
            return request

        # Convert raw dictionaries to Pydantic objects
        requirements = []
        for req in parsed.get("requirements", []):
            requirements.append(
                CustomerRequirement(
                    category=req.get("category", "technical"),
                    name=req.get("name", "Unknown"),
                    value=req.get("value", ""),
                    priority=req.get("priority", "preferred"),
                )
            )

        request = CustomerRequest(
            raw_text=raw_text,
            requirements=requirements,
            workloads=parsed.get("workloads", []),
            vendor_preference=parsed.get("vendor_preference"),
            target_platform=parsed.get("target_platform"),
        )

        logger.info(f"Extracted workloads: {request.workloads}")
        logger.info(f"Extracted requirements: {[req.name for req in requirements]}")

        return request

    # _extract_workloads and _extract_requirements were removed to
    # enforce vendor and category agnosticism via the LLM.
