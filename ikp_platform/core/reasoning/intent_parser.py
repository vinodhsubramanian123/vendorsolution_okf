"""
Intent Parser — Extracts structured engineering requirements from natural language.

Governs: Blueprint 05 §4 (Customer Requirements)

Customer requests SHALL be converted into structured engineering requirements
before reasoning begins.
"""

import re
import logging
from typing import List

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
        # Keywords for workloads
        self.workload_keywords = {
            "ai": ["ai", "machine learning", "deep learning", "inference", "training"],
            "virtualization": ["vmware", "vsphere", "virtualization", "vms"],
            "database": ["sql", "oracle", "database", "db"],
            "sap": ["sap", "hana"],
            "hpc": ["hpc", "high performance computing"],
            "vdi": ["vdi", "virtual desktop", "citrix"],
        }

        # Keywords for components
        self.component_keywords = {
            "gpu": ["gpu", "accelerator", "nvidia", "rtx"],
            "nvme": ["nvme", "flash", "fast storage"],
            "high_memory": ["high memory", "large memory", "tb ram"],
        }

    def parse_request(self, raw_text: str) -> CustomerRequest:
        """Parse natural language into a structured request using LLM."""
        logger.info(f"Parsing customer request: '{raw_text[:50]}...'")

        parsed = self.llm.parse_intent(raw_text)

        # Fallback to heuristics if LLM failed
        if not parsed.get("workloads") and not parsed.get("requirements"):
            logger.info(
                "LLM returned empty or failed. Falling back to heuristic parsing."
            )
            text_lower = raw_text.lower()
            workloads = self._extract_workloads(text_lower)
            requirements = self._extract_requirements(text_lower)
            vendor_preference = None
            if "hpe" in text_lower:
                vendor_preference = "HPE"
            elif "dell" in text_lower:
                vendor_preference = "Dell"

            target_platform = None
            if "alletra" in text_lower:
                target_platform = "alletra"
            elif "dl580" in text_lower:
                target_platform = "dl580"
            elif "dl380" in text_lower:
                target_platform = "dl380"

            request = CustomerRequest(
                raw_text=raw_text,
                requirements=requirements,
                workloads=workloads,
                vendor_preference=vendor_preference,
                target_platform=target_platform,
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

    def _extract_workloads(self, text_lower: str) -> List[str]:
        workloads = set()
        for wkld, keywords in self.workload_keywords.items():
            if any(kw in text_lower for kw in keywords):
                workloads.add(wkld)
        return list(workloads)

    def _extract_requirements(self, text_lower: str) -> List[CustomerRequirement]:
        reqs = []

        # Check for component/technical requirements
        if any(kw in text_lower for kw in self.component_keywords["gpu"]):
            # For GPU, assume required if asked for
            _ = (
                "required"
                if any(w in text_lower for w in ["require", "must", "need", "gpu"])
                else "preferred"
            )
            reqs.append(
                CustomerRequirement(
                    category="technical",
                    name="Accelerator",
                    value="GPU",
                    priority="required",  # Usually required if requested
                )
            )

        if any(kw in text_lower for kw in self.component_keywords["nvme"]):
            # Check if user explicitly required it
            is_required = any(
                w in text_lower for w in ["require", "must", "critical", "mandatory"]
            )
            reqs.append(
                CustomerRequirement(
                    category="technical",
                    name="Storage Protocol",
                    value="NVMe",
                    priority="required" if is_required else "preferred",
                )
            )

        # Check for budget
        budget_match = re.search(r"budget.*?\$?(\d+)[kK]?", text_lower)
        if budget_match:
            val = int(budget_match.group(1))
            if "k" in budget_match.group(0).lower():
                val *= 1000
            reqs.append(
                CustomerRequirement(
                    category="commercial",
                    name="Max Budget",
                    value=val,
                    priority="required",
                )
            )

        return reqs
