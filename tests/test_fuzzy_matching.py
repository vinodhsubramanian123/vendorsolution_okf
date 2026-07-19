import unittest
import networkx as nx
from ikp_platform.core.validation.boq_validator import BOQValidator
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import SKU


class TestFuzzyMatching(unittest.TestCase):
    def setUp(self):
        self.graph_builder = GraphBuilder()
        self.graph_builder.graph = nx.DiGraph()

        # Add SKUs
        sku1 = SKU(id="sku1", part_number="P51174-B21", title="Frame")
        sku2 = SKU(id="sku2", part_number="872957-B21", title="Composer")

        self.graph_builder.add_concept(sku1)
        self.graph_builder.add_concept(sku2)

        self.validator = BOQValidator(self.graph_builder)

    def test_exact_match(self):
        result = self.validator.validate(["P51174-B21"], {"solution_id": "sol1"})
        self.assertTrue(result.is_valid)
        messages = [m for m in result.messages if m.severity != "Warning"]
        self.assertEqual(len(messages), 0)

    def test_fuzzy_match(self):
        # Missing hyphen
        result = self.validator.validate(["P51174B21"], {"solution_id": "sol1"})
        self.assertTrue(result.is_valid)
        messages = [m for m in result.messages if m.severity != "Warning"]
        self.assertEqual(len(messages), 1)
        self.assertIn("Auto-corrected", messages[0].message)

    def test_invalid_match(self):
        result = self.validator.validate(["INVALID-123"], {"solution_id": "sol1"})
        self.assertFalse(result.is_valid)
        messages = [m for m in result.messages if m.severity != "Warning"]
        self.assertEqual(len(messages), 1)
        self.assertIn("Invalid SKU", messages[0].message)


if __name__ == "__main__":
    unittest.main()
