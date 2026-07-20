import pytest
from ikp_platform.core.ontology.models import Component, Platform, CategoryLimit, EngineeringRelationship, RelationshipType
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator

@pytest.fixture
def mock_graph():
    builder = GraphBuilder()
    
    # Platform
    platform = Platform(id="plat-123", title="Test Platform", vendor="HPE", solution_domain="Compute", mandatory_categories=["Chassis", "CPU"])
    builder.add_concept(platform)
    
    # Riser providing PCIe slots
    riser = Component(
        id="plat-123/components/riser1", title="Riser 1", vendor="HPE", component_subcategory="Riser",
        provided_resources={"pcie_slots": 3.0}
    )
    builder.add_concept(riser)
    builder.graph.add_edge("plat-123", riser.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    # GPU consuming PCIe slots
    gpu = Component(
        id="plat-123/components/gpu1", title="GPU 1", vendor="HPE", component_category="Accelerator",
        consumed_resources={"pcie_slots": 1.0}
    )
    builder.add_concept(gpu)
    builder.graph.add_edge("plat-123", gpu.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    # Missing Mandatory CPU Dependency (simulating user forgetting to select it)
    cpu = Component(
        id="plat-123/components/cpu1", title="CPU 1", vendor="HPE", component_category="CPU"
    )
    builder.add_concept(cpu)
    builder.graph.add_edge("plat-123", cpu.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    # CPU Constraint
    cpu_limit = CategoryLimit(
        id="plat-123/limits/min-cpu", title="Min CPU", limit_name="Min CPU",
        limit_value=2, min_qty=1, target_category="CPU"
    )
    builder.add_concept(cpu_limit)
    builder.graph.add_edge("plat-123", cpu_limit.id, relationship_type=RelationshipType.CONTAINS.value)
    
    # Riser Constraint
    riser_limit = CategoryLimit(
        id="plat-123/limits/max-risers", title="Max Risers", limit_name="Max Risers",
        limit_value=2, target_subcategory="Riser"
    )
    builder.add_concept(riser_limit)
    builder.graph.add_edge("plat-123", riser_limit.id, relationship_type=RelationshipType.CONTAINS.value)
    
    return builder

def test_dynamic_math_exhaustion(mock_graph):
    engine = RuleEngine(mock_graph)
    
    # Test valid math (3 slots provided by 1 riser, 2 GPUs consuming 2 slots)
    is_valid, _, errors = engine.evaluate_solution("plat-123", ["plat-123/components/riser1", "plat-123/components/gpu1", "plat-123/components/gpu1", "plat-123/components/cpu1"])
    # Filter out MISSING_REQUIRED_CATEGORY (Chassis) since we just want to test Math
    math_errors = [e for e in errors if "Resource Exhausted" in e.message]
    assert len(math_errors) == 0
    
    # Test invalid math (3 slots provided, 4 GPUs consuming 4 slots)
    is_valid, _, errors = engine.evaluate_solution("plat-123", ["plat-123/components/riser1", "plat-123/components/gpu1", "plat-123/components/gpu1", "plat-123/components/gpu1", "plat-123/components/gpu1"])
    math_errors = [e for e in errors if "Resource Exhausted" in e.message]
    assert len(math_errors) == 1
    assert "Resource Exhausted: Solution requires 4.0 pcie_slots, but only 3.0 pcie_slots" in math_errors[0].message
    assert "Absolute Maximum Theoretical Capacity: 6.0 pcie_slots" in math_errors[0].message

def test_missing_dependency_failure(mock_graph):
    engine = RuleEngine(mock_graph)
    # Test failure when a mandatory dependency (CPU) is missing but constraint requires min_qty=1
    is_valid, _, errors = engine.evaluate_solution("plat-123", ["plat-123/components/riser1"])
    missing_errors = [e for e in errors if e.failure_type.value == "missing_required_category"]
    assert len(missing_errors) > 0
    assert "Constraint violation" in missing_errors[0].message
