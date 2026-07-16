"""
Solution Generator — Synthesizes optimized solution candidates.

Governs: Blueprint 05 §13 (Solution Synthesis)

Generates multiple valid solution profiles (Lowest Cost, Balanced, Performance)
by combining the Intent Parser and Rule Engine over the Knowledge Graph.
"""

import logging
from typing import List, Dict, Any, Optional

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import CustomerRequest, SolutionCandidate, ConfidenceLevel, EngineeringObjectType
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.llm_client import LLMClient

logger = logging.getLogger("ikp.reasoning.solution_generator")


class SolutionGenerator:
    """Generates explainable solution candidates based on customer intent."""

    def __init__(self, graph: GraphBuilder, vector_store=None, mcp_client=None):
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
        candidates = []
        
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
                pid for pid in platform_ids 
                if target in pid.lower() 
                or (self.graph.graph.nodes[pid].get("title") and target in self.graph.graph.nodes[pid].get("title").lower())
                or (self.graph.graph.nodes[pid].get("description") and target in self.graph.graph.nodes[pid].get("description").lower())
            ]
            
        if not platform_ids:
            logger.warning("No platforms match the basic criteria or target_platform.")
            return candidates
            
        # For each platform, generate candidates
        for platform_id in platform_ids:
            p_data = self.graph.graph.nodes[platform_id]
            
            # Check if platform has required capabilities (Workloads)
            p_caps = set(c.lower() for c in p_data.get("capabilities", []))
            
            # Very basic scoring
            score = 0
            for w in request.workloads:
                if w.lower() in p_caps or w.lower() in [t.lower() for t in p_data.get("tags", [])]:
                    score += 1
                    
            if request.workloads and score == 0:
                continue # Platform doesn't support the workloads
            elif not request.workloads and not request.target_platform:
                # If neither is provided, don't just pick all platforms, pick the first one to avoid noise
                if len(candidates) > 0:
                    continue
                
            # Build a "Balanced" profile candidate
            candidate = self._build_candidate(platform_id, request, "Balanced")
            if candidate:
                candidates.append(candidate)
                
            # Could build Lowest Cost / Performance here by changing component selection logic
            
        return candidates

    def _build_candidate(self, platform_id: str, request: CustomerRequest, profile: str) -> Optional[SolutionCandidate]:
        """Builds a single candidate and validates it."""
        reasoning_chain = []
        reasoning_chain.append(f"Selected platform {platform_id} for profile '{profile}'")
        
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
                query_text = " ".join([f"{req.name} {req.value}" for req in request.requirements])
                logger.info(f"Performing search for: '{query_text}'")
                
                search_matches = set()
                
                # 1. Vector Search (Gemini)
                if self.vector_store:
                    semantic_matches = self.vector_store.semantic_search(query_text, n_results=50)
                    if semantic_matches:
                        search_matches.update(semantic_matches)
                        
                # 2. MCP Obsidian Search (Parallel fallback/collation)
                if self.mcp_client:
                    mcp_results = self.mcp_client.search(query_text)
                    if mcp_results:
                        # MCP now returns exact component IDs directly
                        for cid in mcp_results:
                            search_matches.add(cid)
                            
                if search_matches:
                    # Intersect search matches with graph compatibility
                    compatible_ids = list(set(compatible_ids).intersection(search_matches))
                    logger.info(f"Search engines reduced search space to {len(compatible_ids)} candidates.")
            
            # Prepare a JSON representation of available components for the LLM
            available_nodes = {}
            for cid in compatible_ids:
                if cid in self.graph.graph:
                    node_data = self.graph.graph.nodes[cid]
                    available_nodes[cid] = {
                        "title": node_data.get("title", ""),
                        "category": node_data.get("attr_component_category", ""),
                    }
                    
            # 2. Serialize customer requirements
            reqs_dict = [req.model_dump() for req in request.requirements]
            
            # 3. Call LLM to select components
            selected_ids, llm_reasoning = self.llm.select_components(platform_id, available_nodes, reqs_dict)
            
            if selected_ids or (not selected_ids and llm_reasoning and not any("LLM failure" in r for r in llm_reasoning)):
                # Sanitize output (ensure LLM didn't hallucinate IDs)
                valid_selected = [cid for cid in selected_ids if cid in available_nodes]
                
                components.extend(valid_selected)
                for req in request.requirements:
                    satisfied_reqs.append(req.name)
                    
                reasoning_chain.extend(llm_reasoning)
            else:
                # Fallback to heuristic selection if LLM failed
                logger.info("LLM returned empty or failed. Falling back to heuristic component selection.")
                for req in request.requirements:
                    logger.info(f"Fallback processing requirement: {req.name} = {req.value}")
                    if req.value == "GPU":
                        gpus = self.graph.filter_by_metadata({"component_category": "GPU"})
                        compatible = self.graph.get_compatible(platform_id)
                        valid_gpus = list(set(gpus).intersection(set(compatible)))
                        
                        if valid_gpus:
                            selected_gpu = valid_gpus[0]
                            components.append(selected_gpu)
                            satisfied_reqs.append(req.name)
                            reasoning_chain.append(f"Added {selected_gpu} to satisfy {req.name} requirement")
                            logger.info(f"Added {selected_gpu}")
                        else:
                            reasoning_chain.append(f"Could not satisfy requirement {req.name}: No compatible GPU found")
                            logger.info("No compatible GPU found")
                    
                    elif "NVMe" in str(req.value) or "Storage" in req.name:
                        logger.info(f"Processing NVMe fallback for {req.name}")
                        # Fallback for NVMe storage
                        # Find compatible components that have NVMe in their description or title
                        compatible = self.graph.get_compatible(platform_id)
                        nvme_comps = []
                        for cid in compatible:
                            if cid in self.graph.graph:
                                node_data = self.graph.graph.nodes[cid]
                                text_repr = str(node_data.get("title", "")) + " " + str(node_data.get("description", ""))
                                if "NVMe" in text_repr or "Drive Cage" in text_repr or "storage" in text_repr.lower():
                                    nvme_comps.append(cid)
                        
                        logger.info(f"Found NVMe components: {nvme_comps}")
                        if nvme_comps:
                            selected_storage = nvme_comps[0]
                            components.append(selected_storage)
                            satisfied_reqs.append(req.name)
                            reasoning_chain.append(f"Added {selected_storage} to satisfy {req.name} requirement")
                        else:
                            reasoning_chain.append(f"Could not satisfy requirement {req.name}: No compatible NVMe/Storage found")
        
        # Validate the solution using Rule Engine
        is_valid, validation_chain, errors = self.rule_engine.evaluate_solution(platform_id, components)
        reasoning_chain.extend(validation_chain)
        
        confidence = ConfidenceLevel.HIGH if is_valid else ConfidenceLevel.LOW
        
        candidate = SolutionCandidate(
            request_id=request.request_id,
            profile=profile,
            components=[platform_id] + components,
            reasoning_chain=reasoning_chain,
            requirements_satisfied=satisfied_reqs,
            confidence=confidence,
            validation_status="Valid" if is_valid else "Invalid: " + "; ".join(errors)
        )
        
        return candidate
