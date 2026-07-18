"""
Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.

Governs: Blueprint 05 §6 (Metadata Filtering), Blueprint 06 §6 (Knowledge Discovery)

The graph is the active reasoning layer. It mirrors the OKF repository but enables
fast traversal, metadata filtering, and relationship evaluation that would be
impossible with file-based operations alone.
"""

import networkx as nx
from typing import List, Dict, Any, Optional, Set
from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    RelationshipType,
)


class GraphBuilder:
    """
    Maintains an in-memory NetworkX DiGraph representing the canonical
    engineering knowledge base.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    # -------------------------------------------------------------------
    # Node management
    # -------------------------------------------------------------------

    def add_concept(self, obj: BaseEngineeringObject) -> None:
        """Add a concept and all its attributes as a node in the graph."""
        node_attrs = {
            "type": obj.type.value,
            "title": obj.title,
            "description": obj.description,
            "vendor": obj.vendor,
            "solution_domain": obj.solution_domain,
            "product_family": obj.product_family,
            "generation": obj.generation,
            "lifecycle_status": obj.lifecycle_status.value if obj.lifecycle_status else None,
            "tags": obj.tags or [],
            "capabilities": obj.capabilities or [],
        }

        if hasattr(obj, "confidence") and obj.confidence:
            node_attrs["confidence"] = obj.confidence.value if hasattr(obj.confidence, 'value') else obj.confidence
            
        if hasattr(obj, "evidence") and obj.evidence:
            node_attrs["evidence"] = [e.model_dump() if hasattr(e, 'model_dump') else e for e in obj.evidence]

        if hasattr(obj, "component_category") and obj.component_category:
            node_attrs["component_category"] = obj.component_category
            node_attrs["attr_component_category"] = obj.component_category
            
        if hasattr(obj, "component_subcategory") and obj.component_subcategory:
            node_attrs["attr_component_subcategory"] = obj.component_subcategory
            
        if hasattr(obj, "inclusive_qty") and obj.inclusive_qty is not None:
            node_attrs["attr_inclusive_qty"] = obj.inclusive_qty
            
        if hasattr(obj, "target_category") and obj.target_category:
            node_attrs["attr_target_category"] = obj.target_category
            
        if hasattr(obj, "target_subcategory") and obj.target_subcategory:
            node_attrs["attr_target_subcategory"] = obj.target_subcategory

        if hasattr(obj, "performance_requirements") and obj.performance_requirements:
            for k, v in obj.performance_requirements.items():
                node_attrs[f"req_perf_{k}"] = v

        if hasattr(obj, "capacity_requirements") and obj.capacity_requirements:
            for k, v in obj.capacity_requirements.items():
                node_attrs[f"req_cap_{k}"] = v

        if hasattr(obj, "scope") and obj.scope:
            node_attrs["scope"] = obj.scope
            
        if hasattr(obj, "severity") and obj.severity:
            node_attrs["severity"] = obj.severity.value if hasattr(obj.severity, 'value') else obj.severity

        if hasattr(obj, "applicable_objects") and obj.applicable_objects:
            node_attrs["applicable_objects"] = obj.applicable_objects

        if hasattr(obj, "limit_name") and obj.limit_name:
            node_attrs["limit_name"] = obj.limit_name
            node_attrs["limit_value"] = obj.limit_value
            
        if hasattr(obj, "part_number") and obj.part_number:
            node_attrs["attr_part_number"] = obj.part_number

        # Add structured attributes
        for attr in obj.attributes:
            key = f"attr_{attr.name.lower().replace(' ', '_')}"
            node_attrs[key] = attr.value

        self.graph.add_node(obj.id, **node_attrs)

        # Add relationships as directed edges
        for rel in obj.relationships:
            self.graph.add_edge(
                obj.id,
                rel.target_id,
                relationship_type=rel.relationship_type.value,
                evidence=[e.model_dump() for e in rel.evidence] if rel.evidence else [],
                version=rel.version,
            )

    def remove_concept(self, object_id: str) -> None:
        """Remove a concept and all its edges from the graph."""
        if object_id in self.graph:
            self.graph.remove_node(object_id)

    # -------------------------------------------------------------------
    # Metadata filtering — Blueprint 05 §6, Blueprint 06 §6
    # -------------------------------------------------------------------

    def filter_by_metadata(self, criteria: Dict[str, Any]) -> List[str]:
        """
        Filter nodes by metadata attributes.

        Blueprint 05 §6: "Before reasoning begins, the implementation SHALL
        reduce the engineering search space."

        Args:
            criteria: Dict of {attribute_name: expected_value}.
                      Values can be strings (exact match), lists (any match),
                      or None (must be present).

        Returns:
            List of node IDs matching ALL criteria.
        """
        matching = []

        for node_id, attrs in self.graph.nodes(data=True):
            if self._matches_criteria(attrs, criteria):
                matching.append(node_id)

        return matching

    def filter_by_capabilities(self, required_capabilities: List[str]) -> List[str]:
        """Find all nodes that have ALL the required capabilities."""
        matching = []
        required_set = set(c.lower() for c in required_capabilities)

        for node_id, attrs in self.graph.nodes(data=True):
            node_caps = set(c.lower() for c in attrs.get("capabilities", []))
            if required_set.issubset(node_caps):
                matching.append(node_id)

        return matching

    def filter_by_type(self, obj_type: str) -> List[str]:
        """Find all nodes of a given type."""
        return [
            node_id
            for node_id, attrs in self.graph.nodes(data=True)
            if attrs.get("type") == obj_type
        ]

    @staticmethod
    def _matches_criteria(attrs: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if a node's attributes match all criteria."""
        for key, expected in criteria.items():
            actual = attrs.get(key)

            if isinstance(expected, dict) and ("min" in expected or "max" in expected):
                if actual is None:
                    return False
                try:
                    actual_val = float(actual)
                    if "min" in expected and actual_val < float(expected["min"]):
                        return False
                    if "max" in expected and actual_val > float(expected["max"]):
                        return False
                except (ValueError, TypeError):
                    return False
                continue

            if expected is None:
                # Must be present
                if actual is None:
                    return False
            elif isinstance(expected, list):
                # Any match
                if isinstance(actual, list):
                    if not any(e in actual for e in expected):
                        return False
                elif actual not in expected:
                    return False
            else:
                # Exact match (case-insensitive for strings)
                if isinstance(actual, str) and isinstance(expected, str):
                    if actual.lower() != expected.lower():
                        return False
                elif actual != expected:
                    return False

        return True

    # -------------------------------------------------------------------
    # Relationship traversal — Blueprint 05 §8
    # -------------------------------------------------------------------

    def traverse_relationships(
        self,
        node_id: str,
        relationship_type: Optional[str] = None,
        direction: str = "outbound",
    ) -> List[Dict[str, Any]]:
        """
        Traverse relationships from a node, optionally filtered by type.

        Blueprint 05 §8: "The implementation SHALL traverse engineering
        relationships rather than isolated documents."

        Args:
            node_id: Starting node.
            relationship_type: Filter by RelationshipType value (e.g., "Requires").
            direction: "outbound", "inbound", or "both".

        Returns:
            List of dicts with 'source', 'target', 'relationship_type', 'evidence'.
        """
        results = []

        if direction in ("outbound", "both") and node_id in self.graph:
            for _, target, data in self.graph.out_edges(node_id, data=True):
                if relationship_type and data.get("relationship_type") != relationship_type:
                    continue
                results.append({
                    "source": node_id,
                    "target": target,
                    "relationship_type": data.get("relationship_type"),
                    "evidence": data.get("evidence", []),
                })

        if direction in ("inbound", "both") and node_id in self.graph:
            for source, _, data in self.graph.in_edges(node_id, data=True):
                if relationship_type and data.get("relationship_type") != relationship_type:
                    continue
                results.append({
                    "source": source,
                    "target": node_id,
                    "relationship_type": data.get("relationship_type"),
                    "evidence": data.get("evidence", []),
                })

        return results

    def find_paths(self, source_id: str, target_id: str, max_depth: int = 10) -> List[List[str]]:
        """Find all simple paths between two engineering concepts."""
        if source_id in self.graph and target_id in self.graph:
            return list(nx.all_simple_paths(
                self.graph, source_id, target_id, cutoff=max_depth
            ))
        return []

    def get_dependencies(self, object_id: str) -> List[str]:
        """Get all outbound dependency targets (Requires, Depends On)."""
        dep_types = {RelationshipType.REQUIRES.value, RelationshipType.DEPENDS_ON.value}
        results = []
        if object_id in self.graph:
            for _, target, data in self.graph.out_edges(object_id, data=True):
                if data.get("relationship_type") in dep_types:
                    results.append(target)
        return results

    def get_compatible(self, object_id: str) -> List[str]:
        """Get all objects compatible with the given object."""
        return [
            r["target"]
            for r in self.traverse_relationships(
                object_id,
                relationship_type=RelationshipType.COMPATIBLE_WITH.value,
                direction="both",
            )
            if r["target"] != object_id
        ] + [
            r["source"]
            for r in self.traverse_relationships(
                object_id,
                relationship_type=RelationshipType.COMPATIBLE_WITH.value,
                direction="both",
            )
            if r["source"] != object_id
        ]

    # -------------------------------------------------------------------
    # Graph statistics — Blueprint 02 §11 (Observability)
    # -------------------------------------------------------------------

    def get_stats(self) -> Dict[str, int]:
        """Return graph statistics for observability."""
        type_counts: Dict[str, int] = {}
        for _, attrs in self.graph.nodes(data=True):
            t = attrs.get("type", "Unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "type_counts": type_counts,
        }
