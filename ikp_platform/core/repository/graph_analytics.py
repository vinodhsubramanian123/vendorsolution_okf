"""
Graph Analytics Engine — Advanced network analysis for the Knowledge Graph.

Governs: Analytics for Root-Cause Detection, Fragility Analysis, 
         Subgraph Matching, and Gap Analysis Scoring.
"""

import networkx as nx
from typing import List, Dict, Any
from ikp_platform.core.repository.graph_builder import GraphBuilder


class GraphAnalyticsEngine:
    """
    Provides advanced graph algorithms for analyzing the engineering ontology,
    such as identifying fragile mappings (articulation points) and scoring
    vendor solutions using subgraph heuristics.
    """

    def __init__(self, graph_builder: GraphBuilder):
        self.gb = graph_builder
        self.graph = graph_builder.graph

    def get_articulation_points(self) -> List[str]:
        """
        Find all articulation points (cut vertices) in the knowledge graph.
        An articulation point is a node whose removal disconnects the graph,
        indicating a fragile mapping or a critical root-cause bottleneck.
        """
        # Articulation points are mathematically defined on undirected graphs
        undirected_g = self.graph.to_undirected()
        return [str(node) for node in nx.articulation_points(undirected_g)]

    def get_fragility_report(self) -> Dict[str, Any]:
        """
        Generate a report on graph fragility based on articulation points.
        Returns the top critical nodes and their degree (impact radius).
        """
        ap_nodes = self.get_articulation_points()

        # Rank by degree to see which articulation point connects the most nodes
        ap_ranked = []
        for node in ap_nodes:
            degree = self.graph.degree(node)
            node_data = self.graph.nodes.get(node, {})
            node_type = node_data.get("type", "Unknown")
            ap_ranked.append(
                {
                    "node_id": node,
                    "type": node_type,
                    "degree": degree,
                    "name": node_data.get("name", node),
                }
            )

        ap_ranked.sort(key=lambda x: x["degree"], reverse=True)

        return {
            "total_articulation_points": len(ap_nodes),
            "critical_nodes": ap_ranked[:20],  # top 20 most impactful
        }

    def check_subgraph_isomorphism(
        self, boq_graph: nx.DiGraph, bom_graph: nx.DiGraph
    ) -> bool:
        """
        Check if the BOQ (Bill of Quantities) structure exists entirely within
        the BOM (Bill of Materials) structure using Subgraph Isomorphism.

        This effectively answers: "Does this requested topology exist inside 
        our generated solution?"
        """

        def node_match(n1: Dict[str, Any], n2: Dict[str, Any]) -> bool:
            # n1 is BOM node, n2 is BOQ node
            t1 = n1.get("type")
            t2 = n2.get("type")
            cat1 = n1.get("attr_component_category")
            cat2 = n2.get("attr_component_category")

            if t1 and t2 and t1 != t2:
                return False
            # If the customer requested a specific category, the BOM must match it
            if cat2 and cat1 != cat2:
                return False
            return True

        matcher = nx.isomorphism.DiGraphMatcher(
            bom_graph, boq_graph, node_match=node_match
        )
        return matcher.subgraph_is_monomorphic()

    def compute_vendor_solution_score(
        self, boq_nodes: List[Dict[str, Any]], bom_nodes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Heuristic "Vendor Solution Match Score" (inspired by Graph Edit Distance).
        Instead of computationally expensive pure GED, this applies business weights.

        Calculates the overlap between what the customer requested (BOQ) and 
        what the solution contains (BOM).
        """
        boq_categories = [
            n.get("attr_component_category")
            for n in boq_nodes
            if n.get("attr_component_category")
        ]
        bom_categories = [
            n.get("attr_component_category")
            for n in bom_nodes
            if n.get("attr_component_category")
        ]

        # Calculate base overlap
        matched_categories = 0
        bom_cat_copy = bom_categories.copy()
        for cat in boq_categories:
            if cat in bom_cat_copy:
                matched_categories += 1
                bom_cat_copy.remove(cat)

        component_match_score = (
            (matched_categories / len(boq_categories)) if boq_categories else 1.0
        )

        # Weighted Business Importance (e.g., Core Compute/Storage is prioritized)
        critical_categories = {
            "GPU",
            "CPU",
            "Processor",
            "Accelerator",
            "Memory",
            "Storage",
            "Controller"
        }
        critical_boq = [c for c in boq_categories if c in critical_categories]
        critical_bom = [c for c in bom_categories if c in critical_categories]

        matched_critical = 0
        crit_bom_copy = critical_bom.copy()
        for cat in critical_boq:
            if cat in crit_bom_copy:
                matched_critical += 1
                crit_bom_copy.remove(cat)

        critical_match_score = (
            (matched_critical / len(critical_boq)) if critical_boq else 1.0
        )

        # 60% Critical Match, 40% Base Component Match
        total_score = (component_match_score * 0.4) + (critical_match_score * 0.6)

        missing = list(set(boq_categories) - set(bom_categories))

        return {
            "score": round(total_score, 4),
            "component_match_ratio": round(component_match_score, 4),
            "critical_match_ratio": round(critical_match_score, 4),
            "missing_categories": missing,
        }
