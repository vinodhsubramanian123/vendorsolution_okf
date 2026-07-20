import pytest
from ikp_platform.core.ontology.models import Component, Platform, CategoryLimit, EngineeringRelationship, RelationshipType
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.reasoning.rule_engine import RuleEngine

@pytest.fixture
def negative_test_graph():
    builder = GraphBuilder()
    
    # Base Platform
    platform = Platform(id="plat-neg", title="Negative Test Platform", vendor="HPE", solution_domain="Compute", mandatory_categories=["Chassis"])
    builder.add_concept(platform)
    
    # 1. Components for Incompatibility Test
    comp_a = Component(id="plat-neg/comp-a", title="Component A", component_category="Networking")
    comp_b = Component(id="plat-neg/comp-b", title="Component B", component_category="Networking")
    builder.add_concept(comp_a)
    builder.add_concept(comp_b)
    builder.graph.add_edge("plat-neg", comp_a.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    builder.graph.add_edge("plat-neg", comp_b.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    # Add mutual exclusion
    builder.graph.add_edge(comp_a.id, comp_b.id, relationship_type=RelationshipType.INCOMPATIBLE_WITH.value)
    
    # 2. Components for Subcategory Limit (Storage Controller Max = 1)
    controller1 = Component(id="plat-neg/ctrl-1", title="Controller 1", component_category="Storage", component_subcategory="Storage Controller")
    controller2 = Component(id="plat-neg/ctrl-2", title="Controller 2", component_category="Storage", component_subcategory="Storage Controller")
    builder.add_concept(controller1)
    builder.add_concept(controller2)
    builder.graph.add_edge("plat-neg", controller1.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    builder.graph.add_edge("plat-neg", controller2.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    ctrl_limit = CategoryLimit(
        id="plat-neg/limits/max-ctrl", title="Max Storage Controller", limit_name="Max Storage Controller",
        limit_value=1, target_subcategory="Storage Controller"
    )
    builder.add_concept(ctrl_limit)
    builder.graph.add_edge("plat-neg", ctrl_limit.id, relationship_type=RelationshipType.CONTAINS.value)
    
    # 3. Components for Resource Ceiling Break (Networking slots)
    riser = Component(
        id="plat-neg/riser", title="Primary Riser", component_category="Riser", component_subcategory="Riser",
        provided_resources={"networking_slots": 4.0}
    )
    net_card = Component(
        id="plat-neg/net-card", title="100Gb NIC", component_category="Networking",
        consumed_resources={"networking_slots": 1.0}
    )
    builder.add_concept(riser)
    builder.add_concept(net_card)
    builder.graph.add_edge("plat-neg", riser.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    builder.graph.add_edge("plat-neg", net_card.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    # Riser max limit = 2 (theoretical ceiling = 2 * 4 = 8 networking slots)
    riser_limit = CategoryLimit(
        id="plat-neg/limits/max-risers", title="Max Risers", limit_name="Max Risers",
        limit_value=2, target_subcategory="Riser"
    )
    builder.add_concept(riser_limit)
    builder.graph.add_edge("plat-neg", riser_limit.id, relationship_type=RelationshipType.CONTAINS.value)
    
    # 4. Missing Dependency Chain (Min CPUs = 2)
    cpu = Component(id="plat-neg/cpu-1", title="CPU 1", component_category="CPU")
    builder.add_concept(cpu)
    builder.graph.add_edge("plat-neg", cpu.id, relationship_type=RelationshipType.COMPATIBLE_WITH.value)
    
    cpu_limit = CategoryLimit(
        id="plat-neg/limits/min-cpu", title="Dual CPU Required", limit_name="Min CPUs",
        min_qty=2, limit_value=4, target_category="CPU"
    )
    builder.add_concept(cpu_limit)
    builder.graph.add_edge("plat-neg", cpu_limit.id, relationship_type=RelationshipType.CONTAINS.value)
    
    return builder

def test_incompatible_components(negative_test_graph):
    engine = RuleEngine(negative_test_graph)
    is_valid, _, errors = engine.evaluate_solution("plat-neg", ["plat-neg/comp-a", "plat-neg/comp-b"])
    
    assert not is_valid
    incompatible_errors = [e for e in errors if e.failure_type.value == "incompatible"]
    assert len(incompatible_errors) == 1
    assert "plat-neg/comp-a is incompatible with plat-neg/comp-b" in incompatible_errors[0].message

def test_subcategory_limit_exceeded(negative_test_graph):
    engine = RuleEngine(negative_test_graph)
    is_valid, _, errors = engine.evaluate_solution("plat-neg", ["plat-neg/ctrl-1", "plat-neg/ctrl-2"])
    
    assert not is_valid
    limit_errors = [e for e in errors if e.failure_type.value == "category_limit_exceeded" and "storage controller" in getattr(e, "message", "").lower()]
    assert len(limit_errors) == 1
    assert "Constraint violation: max storage controller (Max: 1, Requested: 2)" in limit_errors[0].message

def test_resource_ceiling_broken(negative_test_graph):
    engine = RuleEngine(negative_test_graph)
    # Riser provides 4 slots. We request 1 riser and 9 network cards.
    # The ceiling is 8 (2 risers * 4). We are requesting 9.
    components = ["plat-neg/riser"] + ["plat-neg/net-card"] * 9
    is_valid, _, errors = engine.evaluate_solution("plat-neg", components)
    
    assert not is_valid
    math_errors = [e for e in errors if "Resource Exhausted" in getattr(e, "message", "")]
    assert len(math_errors) == 1
    msg = math_errors[0].message
    assert "Solution requires 9.0 networking_slots" in msg
    assert "Absolute Maximum Theoretical Capacity: 8.0 networking_slots" in msg

def test_missing_minimum_quantity(negative_test_graph):
    engine = RuleEngine(negative_test_graph)
    # Requesting only 1 CPU when the rule mandates min_qty=2
    is_valid, _, errors = engine.evaluate_solution("plat-neg", ["plat-neg/cpu-1"])
    
    assert not is_valid
    missing_errors = [e for e in errors if e.failure_type.value == "missing_required_category"]
    assert len(missing_errors) > 0
    cpu_error = [e for e in missing_errors if "min cpus" in getattr(e, "message", "").lower()]
    assert len(cpu_error) == 1
    assert "Constraint violation: min cpus (Min: 2, Requested: 1)" in cpu_error[0].message
    
def test_remediation_engine(negative_test_graph):
    from ikp_platform.core.reasoning.remediation_engine import RemediationEngine
    from ikp_platform.core.validation.pipeline import ValidationPipeline, ValidationContext
    
    pipeline = ValidationPipeline([
        RuleEngine(negative_test_graph),
        RemediationEngine(negative_test_graph)
    ])
    
    ctx1 = ValidationContext(platform_id="plat-neg", original_components=["plat-neg/cpu-1"])
    ctx1 = pipeline.execute(ctx1)
    
    # Check that RuleEngine internally calls RemediationEngine and populates remediations
    cpu_error = [e for e in ctx1.errors if "min cpus" in getattr(e, "message", "").lower()][0]
    assert len(cpu_error.remediations) > 0
    assert any("CPU 1" in rem for rem in cpu_error.remediations)
    
    # Test ceiling break remediation
    components = ["plat-neg/riser"] + ["plat-neg/net-card"] * 9
    ctx2 = ValidationContext(platform_id="plat-neg", original_components=components)
    ctx2 = pipeline.execute(ctx2)
    
    math_errors = [e for e in ctx2.errors if "Resource Exhausted" in getattr(e, "message", "")]
    assert len(math_errors[0].remediations) > 0
    assert any("Primary Riser" in rem for rem in math_errors[0].remediations)
