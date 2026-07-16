import unittest
import networkx as nx
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import Platform, Component, CategoryLimit, EngineeringRelationship, RelationshipType

class TestCategoryLimits(unittest.TestCase):
    def setUp(self):
        self.graph = GraphBuilder()
        self.graph.graph = nx.DiGraph()
        
        self.platform = Platform(id="plat1", title="Platform 1")
        self.graph.add_concept(self.platform)
        
        # Add limit: max 2 Risers
        self.limit = CategoryLimit(
            id="limit1",
            title="Max Risers",
            limit_name="Maximum Riser",
            limit_value=2,
            target_category="Infrastructure",
            target_subcategory="Riser",
            relationships=[EngineeringRelationship(target_id=self.platform.id, relationship_type=RelationshipType.CONTAINS)]
        )
        self.graph.add_concept(self.limit)
        
        self.engine = RuleEngine(self.graph)

    def test_within_limit(self):
        # Create 1 Riser
        riser1 = Component(id="riser1", title="Riser 1", component_category="Infrastructure", component_subcategory="Riser")
        self.graph.add_concept(riser1)
        
        is_valid, chain, errors = self.engine.evaluate_solution(self.platform.id, [riser1.id])
        self.assertEqual(len(errors), 0)

    def test_exceeds_limit(self):
        riser1 = Component(id="riser1", title="Riser 1", component_category="Infrastructure", component_subcategory="Riser", inclusive_qty=3)
        self.graph.add_concept(riser1)
        
        is_valid, chain, errors = self.engine.evaluate_solution(self.platform.id, [riser1.id])
        self.assertEqual(len(errors), 1)
        self.assertIn("Constraint violation", errors[0])

if __name__ == '__main__':
    unittest.main()
