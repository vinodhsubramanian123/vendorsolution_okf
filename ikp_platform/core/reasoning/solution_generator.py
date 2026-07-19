"""
Solution Generator — Synthesizes optimized solution candidates.

Governs: Blueprint 05 §13 (Solution Synthesis)

Generates multiple valid solution profiles (Lowest Cost, Balanced, Performance)
by combining the Intent Parser and Rule Engine over the Knowledge Graph.
"""

import logging
from typing import List, Any, Optional
import concurrent.futures

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import (
    CustomerRequest,
    SolutionCandidate,
    ConfidenceLevel,
    EngineeringObjectType,
)
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.llm_client import LLMClient

logger = logging.getLogger("ikp.reasoning.solution_generator")


class SolutionGenerator:
    """Generates explainable solution candidates based on customer intent."""

    def __init__(
        self,
        graph: GraphBuilder,
        vector_store: Optional[Any] = None,
        mcp_client: Optional[Any] = None,
    ):
        self.graph = graph
        self.vector_store = vector_store
        self.mcp_client = mcp_client
        self.rule_engine = RuleEngine(graph)
        self.llm = LLMClient()

    def generate(self, request: CustomerRequest) -> List[SolutionCandidate]:
        """
        Generate multiple solution profiles.
        Blueprint 05 §13: Where appropriate, solution profiles SHOULD include:
        Lowest Cost, Balanced, Performance Optimized.
        """
        candidates: List[SolutionCandidate] = []

        # 1. Reduce Search Space (Blueprint 05 §6)
        criteria = {}
        if request.vendor_preference:
            criteria["vendor"] = request.vendor_preference

        # We find applicable platforms based on intent
        platform_ids = self.graph.filter_by_type(EngineeringObjectType.PLATFORM.value)

        if criteria:
            filtered = self.graph.filter_by_metadata(criteria)
            platform_ids = list(set(platform_ids).intersection(set(filtered)))

        if request.target_platform:
            target = request.target_platform.lower()
            platform_ids = [
                pid
                for pid in platform_ids
                if target in pid.lower()
                or (
                    self.graph.graph.nodes[pid].get("title")
                    and target in self.graph.graph.nodes[pid].get("title").lower()
                )
                or (
                    self.graph.graph.nodes[pid].get("description")
                    and target in self.graph.graph.nodes[pid].get("description").lower()
                )
            ]

        if not platform_ids:
            logger.warning("No platforms match the basic criteria or target_platform.")
            return candidates

        # For each platform, collect arguments for parallel generation
        tasks = []
        for platform_id in platform_ids:
            p_data = self.graph.graph.nodes[platform_id]

            # Check if platform has required capabilities (Workloads)
            p_caps = set(c.lower() for c in p_data.get("capabilities", []))

            # Very basic scoring
            score = 0
            for w in request.workloads:
                if w.lower() in p_caps or w.lower() in [
                    t.lower() for t in p_data.get("tags", [])
                ]:
                    score += 1

            if request.workloads and score == 0:
                continue  # Platform doesn't support the workloads
            elif not request.workloads and not request.target_platform:
                # If neither is provided, don't just pick all platforms, pick the first one to avoid noise
                if len(tasks) > 0:
                    continue

            tasks.append((platform_id, request, "Balanced"))
            tasks.append((platform_id, request, "Lowest Cost"))
            tasks.append((platform_id, request, "Performance Optimized"))

        if not tasks:
            return candidates

        # Execute candidate generation in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(tasks))) as executor:
            futures = [
                executor.submit(self._build_candidate, p_id, req, prof)
                for p_id, req, prof in tasks
            ]
            for future in concurrent.futures.as_completed(futures):
                candidate = future.result()
                if candidate:
                    candidates.append(candidate)

        return candidates

    def _build_candidate(
        self, platform_id: str, request: CustomerRequest, profile: str
    ) -> Optional[SolutionCandidate]:
        """Builds a single candidate and validates it."""
        reasoning_chain = []
        reasoning_chain.append(
            f"Selected platform {platform_id} for profile '{profile}'"
        )

        # Select compatible components
        # For a real implementation, we would solve a constraint satisfaction problem (CSP)
        # For V1, we just pick the first compatible components that meet requirements

        components = []
        satisfied_reqs = []

        if request.requirements:
            # 1. Fetch all components compatible with platform
            compatible_ids = self.graph.get_compatible(platform_id)

            # If we have a vector store or MCP client, use semantic/full-text search to massively reduce the search space
            if self.vector_store or self.mcp_client:
                query_text = " ".join(
                    [f"{req.name} {req.value}" for req in request.requirements]
                )
                logger.info(f"Performing search for: '{query_text}'")

                search_matches = set()

                # 1. Vector Search (Gemini)
                if self.vector_store:
                    semantic_matches = self.vector_store.semantic_search(
                        query_text, n_results=50
                    )
                    if semantic_matches:
                        search_matches.update({res_id for res_id, _ in semantic_matches})

                # 2. MCP Obsidian Search (Parallel fallback/collation)
                if self.mcp_client:
                    mcp_results = self.mcp_client.search(query_text)
                    if mcp_results:
                        # MCP now returns exact component IDs directly
                        for cid in mcp_results:
                            search_matches.add(cid)

                if search_matches:
                    # Intersect search matches with graph compatibility
                    compatible_ids = list(
                        set(compatible_ids).intersection(search_matches)
                    )
                    logger.info(
                        f"Search engines reduced search space to {len(compatible_ids)} candidates."
                    )

            # Gap 5.3: Sort compatible_ids by component weight (core-first)
            compatible_ids = sorted(
                compatible_ids,
                key=lambda x: (
                    float(self.graph.graph.nodes[x].get("attr_component_weight", 0))
                    if x in self.graph.graph
                    else 0
                ),
                reverse=True,
            )

            # Prepare a JSON representation of available components for the LLM
            available_nodes = {}
            for cid in compatible_ids:
                if cid in self.graph.graph:
                    node_data = self.graph.graph.nodes[cid]
                    available_nodes[cid] = {
                        "title": node_data.get("title", ""),
                        "category": node_data.get("attr_component_category", ""),
                        "weight": node_data.get("attr_component_weight", 0),
                    }

            # 2. Serialize customer requirements
            reqs_dict = [req.model_dump() for req in request.requirements]

            # 3. Call LLM to select components
            selected_ids, llm_reasoning, newly_satisfied = self.llm.select_components(
                platform_id, available_nodes, reqs_dict, profile
            )

            if selected_ids or (
                not selected_ids
                and llm_reasoning
                and not any("LLM failure" in r for r in llm_reasoning)
            ):
                # Sanitize output (ensure LLM didn't hallucinate IDs)
                valid_selected = [cid for cid in selected_ids if cid in available_nodes]

                components.extend(valid_selected)
                satisfied_reqs.extend(newly_satisfied)

                reasoning_chain.extend(llm_reasoning)
            else:
                # Fallback to heuristic selection if LLM failed
                logger.info(
                    "LLM returned empty or failed. Falling back to heuristic component selection."
                )
                for req in request.requirements:
                    logger.info(
                        f"Fallback processing requirement: {req.name} = {req.value}"
                    )
                    # Generic fallback: match requirement name or value against component metadata
                    compatible = self.graph.get_compatible(platform_id)
                    matches = []
                    search_term = str(req.value).lower()
                    cat_term = req.name.lower()

                    for cid in compatible:
                        if cid in self.graph.graph:
                            node_data = self.graph.graph.nodes[cid]
                            text_repr = (
                                str(node_data.get("title", ""))
                                + " "
                                + str(node_data.get("description", ""))
                            ).lower()
                            cat = str(
                                node_data.get("attr_component_category", "")
                            ).lower()

                            # Check for keyword matches in text or category
                            if (
                                search_term == cat
                                or search_term in text_repr
                                or cat_term in text_repr
                                or cat_term in cat
                            ):
                                matches.append(cid)

                    if matches:
                        selected = matches[0]
                        components.append(selected)
                        satisfied_reqs.append(req.name)
                        reasoning_chain.append(
                            f"Added {selected} to satisfy {req.name} requirement"
                        )
                        logger.info(
                            f"Added {selected} via generic fallback for {req.name}"
                        )
                    else:
                        reasoning_chain.append(
                            f"Could not satisfy requirement {req.name}: No compatible component found"
                        )
                        logger.info(f"No compatible component found for {req.name}")

        # Validate the solution using Rule Engine
        is_valid, validation_chain, errors = self.rule_engine.evaluate_solution(
            platform_id, components
        )
        reasoning_chain.extend(validation_chain)

        confidence = ConfidenceLevel.HIGH if is_valid else ConfidenceLevel.LOW

        candidate = SolutionCandidate(
            request_id=request.request_id,
            profile=profile,
            components=[platform_id] + components,
            reasoning_chain=reasoning_chain,
            requirements_satisfied=satisfied_reqs,
            confidence=confidence,
            validation_status="Valid" if is_valid else "Invalid: " + "; ".join(errors),
        )

        return candidate
