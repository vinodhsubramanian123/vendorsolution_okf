import networkx as nx
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import (
    Platform,
    Component,
    CategoryLimit,
    EngineeringRelationship,
    RelationshipType,
)

graph = GraphBuilder()
graph.graph = nx.DiGraph()

platform = Platform(id="plat1", title="Platform 1")
graph.add_concept(platform)

limit = CategoryLimit(
    id="limit1",
    title="Max Risers",
    limit_name="Maximum Riser",
    limit_value=2,
    target_category="Infrastructure",
    target_subcategory="Riser",
    relationships=[
        EngineeringRelationship(
            target_id=platform.id, relationship_type=RelationshipType.CONTAINS
        )
    ],
)
graph.add_concept(limit)

engine = RuleEngine(graph)

riser1 = Component(
    id="riser1",
    title="Riser 1",
    component_category="Infrastructure",
    component_subcategory="Riser",
    inclusive_qty=3,
)
graph.add_concept(riser1)

is_valid, chain, errors = engine.evaluate_solution(platform.id, [riser1.id])
print("Errors:", errors)
print("Chain:")
for c in chain:
    print(c)
