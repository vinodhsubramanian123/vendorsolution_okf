"""
Graph Builder — In-memory NetworkX knowledge graph with metadata filtering.

Governs: Blueprint 05 §6 (Metadata Filtering), Blueprint 06 §6 (Knowledge Discovery)

The graph is the active reasoning layer. It mirrors the OKF repository but enables
fast traversal, metadata filtering, and relationship evaluation that would be
impossible with file-based operations alone.
"""

import networkx as nx
from typing import List, Dict, Any, Optional
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
        """Add a concept and all its attributes as a node in the graph.

        Field mapping strategy (2026-07-18 audit / see .agents/rules/graph_serialization.md):
        node_attrs is derived from a full ``model_dump`` of the object rather than a
        hand-maintained allowlist of ``hasattr`` checks. The old allowlist pattern
        silently dropped fields THREE separate times as the ontology grew:
          - ``description`` / ``applicable_objects`` (fixed by ADR-001)
          - ``target_subcategory`` / ``component_subcategory`` / ``inclusive_qty``
            (fixed by commit a6ef5df — "CategoryLimit Serialization Issue")
          - ``platform_id`` was found still-missing during the 2026-07-18 audit,
            silently breaking the Rule dedup check in
            ``RepoManager.add_concept`` (it compares
            ``data.get("platform_id") == obj.platform_id``, which could never
            match because the key was never written).
        Dumping every field automatically closes this whole bug class: any field
        added to any ontology subclass now reaches the graph without a manual
        edit here. tests/test_graph_field_parity.py is the regression guard —
        it fails loudly if a future refactor reintroduces an allowlist.
        """
        # Full field dump; enums -> their .value, datetimes -> ISO strings.
        # `attributes`/`relationships`/`history` are handled separately below
        # (structured lists that need their own transformation, not flat scalars).
        node_attrs: Dict[str, Any] = obj.model_dump(
            mode="json", exclude={"attributes", "relationships", "history"}
        )

        node_attrs["tags"] = node_attrs.get("tags") or []
        node_attrs["capabilities"] = node_attrs.get("capabilities") or []

        # Historical `attr_*` aliases some rules/filters key off directly —
        # kept alongside the plain field name for backward compatibility.
        for field, alias in (
            ("component_category", "attr_component_category"),
            ("component_subcategory", "attr_component_subcategory"),
            ("inclusive_qty", "attr_inclusive_qty"),
            ("target_category", "attr_target_category"),
            ("target_subcategory", "attr_target_subcategory"),
            ("part_number", "attr_part_number"),
        ):
            if node_attrs.get(field) is not None:
                node_attrs[alias] = node_attrs[field]

        # Requirement dicts (Workload) get flattened with their historical prefixes.
        for k, v in (getattr(obj, "performance_requirements", None) or {}).items():
            node_attrs[f"req_perf_{k}"] = v
        for k, v in (getattr(obj, "capacity_requirements", None) or {}).items():
            node_attrs[f"req_cap_{k}"] = v

        # NOTE: `evidence` is NOT in the exclude set above, so it's already
        # present in node_attrs, correctly serialized (nested EvidenceRecord
        # models -> dicts, datetimes -> ISO strings) by the top-level
        # model_dump call. No separate handling needed here.

        # Structured `attributes` list -> attr_<name> keys (Blueprint 03 §5).
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
                if (
                    relationship_type
                    and data.get("relationship_type") != relationship_type
                ):
                    continue
                results.append(
                    {
                        "source": node_id,
                        "target": target,
                        "relationship_type": data.get("relationship_type"),
                        "evidence": data.get("evidence", []),
                    }
                )

        if direction in ("inbound", "both") and node_id in self.graph:
            for source, _, data in self.graph.in_edges(node_id, data=True):
                if (
                    relationship_type
                    and data.get("relationship_type") != relationship_type
                ):
                    continue
                results.append(
                    {
                        "source": source,
                        "target": node_id,
                        "relationship_type": data.get("relationship_type"),
                        "evidence": data.get("evidence", []),
                    }
                )

        return results

    def find_paths(
        self, source_id: str, target_id: str, max_depth: int = 10
    ) -> List[List[str]]:
        """Find all simple paths between two engineering concepts."""
        if source_id in self.graph and target_id in self.graph:
            return list(
                nx.all_simple_paths(self.graph, source_id, target_id, cutoff=max_depth)
            )
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

    def get_related(
        self, node_id: str, relationship_type: Optional[str] = None
    ) -> List[str]:
        """
        Get all related node IDs traversing both inbound and outbound edges.

        This prevents bugs where relationship direction is inconsistent
        (e.g., Contains can be platform->component or component->platform).
        """
        related = set()
        for r in self.traverse_relationships(
            node_id, relationship_type, direction="both"
        ):
            other_id = r["target"] if r["source"] == node_id else r["source"]
            if other_id != node_id:
                related.add(other_id)
        return list(related)

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
    # Subgraph generation
    # -------------------------------------------------------------------

    def build_subgraph(self, node_ids: List[str]) -> nx.DiGraph:
        """
        Return an induced subgraph containing only the specified nodes and the
        edges between them. This is useful for passing a narrowed context to
        the LLM reasoning engine.

        Args:
            node_ids: List of node IDs to include.

        Returns:
            A new NetworkX DiGraph containing the induced subgraph.
        """
        return self.graph.subgraph(node_ids).copy()

    # -------------------------------------------------------------------
    # Graph statistics — Blueprint 02 §11 (Observability)
    # -------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
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

    # -------------------------------------------------------------------
    # Structured queries — Phase 3: Search & Ranking
    # -------------------------------------------------------------------

    def filter_by_category(
        self,
        platform_id=None,
        category=None,
        subcategory=None,
        obj_type="Component",
    ):
        """Return all nodes matching the given platform/category/subcategory filters.
        Returns list of dicts with node_id and full node attributes.
        """
        results = []
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get("type") != obj_type:
                continue
            if platform_id:
                node_platform = attrs.get("platform_id") or ""
                if platform_id.lower() not in node_platform.lower() and not node_id.startswith(platform_id):
                    continue
            if category:
                node_cat = (attrs.get("component_category") or attrs.get("attr_component_category") or "").lower()
                if category.lower() not in node_cat:
                    continue
            if subcategory:
                node_subcat = (attrs.get("component_subcategory") or attrs.get("attr_component_subcategory") or "").lower()
                if subcategory.lower() not in node_subcat:
                    continue
            results.append({"id": node_id, **attrs})
        return results

    def get_platform_bill_of_materials(self, platform_id):
        """Return all components and SKUs for a platform, grouped by category."""
        bom = {}
        for node_id, attrs in self.graph.nodes(data=True):
            node_type = attrs.get("type")
            if node_type not in ("Component", "SKU"):
                continue
            node_platform = attrs.get("platform_id") or ""
            if platform_id.lower() not in node_platform.lower() and not node_id.startswith(platform_id):
                continue
            category = (
                attrs.get("component_category")
                or attrs.get("attr_component_category")
                or "Uncategorized"
            )
            if category not in bom:
                bom[category] = []
            bom[category].append({
                "id": node_id,
                "title": attrs.get("title", node_id),
                "description": attrs.get("description", ""),
                "subcategory": attrs.get("component_subcategory") or attrs.get("attr_component_subcategory"),
                "part_number": attrs.get("part_number") or attrs.get("attr_part_number"),
                "confidence": attrs.get("confidence"),
                "lifecycle_status": attrs.get("lifecycle_status"),
                "type": node_type,
            })
        for cat in bom:
            bom[cat] = sorted(bom[cat], key=lambda x: x["title"] or "")
        return bom
