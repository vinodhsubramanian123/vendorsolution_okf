from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import CategoryLimit, Component

g = GraphBuilder()
limit = CategoryLimit(
    id="limit1",
    title="Max Risers",
    limit_name="Maximum Riser",
    limit_value=2,
    target_category="Infrastructure",
    target_subcategory="Riser",
)
g.add_concept(limit)
riser1 = Component(
    id="riser1",
    title="Riser 1",
    component_category="Infrastructure",
    component_subcategory="Riser",
    inclusive_qty=3,
)
g.add_concept(riser1)

print("Limit node data:")
print(g.graph.nodes["limit1"])
print("Riser node data:")
print(g.graph.nodes["riser1"])
