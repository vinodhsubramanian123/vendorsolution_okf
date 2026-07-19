import pytest
from unittest.mock import MagicMock
from ikp_platform.core.workflow.executor import WorkflowExecutor
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import (
    Platform,
    Workload,
    EngineeringRelationship,
    RelationshipType,
    CustomerRequest,
    Component,
    CustomerRequirement,
)
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator

@pytest.fixture
def test_graph():
    """Create a graph for offline headless synthesis testing."""
    graph = GraphBuilder()

    # Workload
    wl = Workload(id="wl-ai", title="AI Workload", solution_domain="Compute")
    graph.add_concept(wl)

    # Platform
    plat = Platform(
        id="hpe-proliant-dl380-gen12",
        title="DL380",
        capabilities=["wl-ai"],
        relationships=[EngineeringRelationship(target_id="wl-ai", relationship_type=RelationshipType.SUPPORTS)]
    )
    graph.add_concept(plat)

    # CPU
    cpu = Component(
        id="hpe-proliant-dl380-gen12-processors-xeon-6505p",
        title="Xeon 6505P",
        component_category="CPU",
        relationships=[EngineeringRelationship(target_id="hpe-proliant-dl380-gen12", relationship_type=RelationshipType.COMPATIBLE_WITH)]
    )
    graph.add_concept(cpu)

    # Memory
    mem = Component(
        id="hpe-proliant-dl380-gen12-components-6000mt",
        title="6000MT Memory",
        component_category="MEMORY",
        relationships=[EngineeringRelationship(target_id="hpe-proliant-dl380-gen12", relationship_type=RelationshipType.COMPATIBLE_WITH)]
    )
    graph.add_concept(mem)

    return graph

def test_headless_negative_scenario_bad_sku(test_graph):
    """Test providing a completely invalid SKU. Workflow should drop it and find valid alternates."""
    executor = WorkflowExecutor(test_graph)
    
    # We simulate a bad SKU requirement
    req = CustomerRequest(
        request_id="test-1",
        workloads=["wl-ai"],
        requirements=[
            CustomerRequirement(category="technical", name="SKU", value="BAD-SKU-999")
        ]
    )
    executor.parser.parse_request = MagicMock(return_value=req)
    
    # We need to simulate the LLM not finding BAD-SKU-999 but returning standard fallback logic.
    # The heuristic fallback will fail to find BAD-SKU-999.
    # The Rule Engine will validate and see it's missing mandatory categories.
    
    # We must actually provide a BOQValidator to the nodes or rely on validate_bom logic.
    # Wait, the WorkflowExecutor uses rule_engine. boq_validator is separate.
    # For headless synthesis, validate_bom uses rule_engine.
    # Let's intercept rule_engine to return an error for BAD-SKU-999.
    from ikp_platform.core.ontology.models import ValidationFailure, ValidationFailureType
    
    def mock_evaluate(platform_id, components):
        errors = []
        if "BAD-SKU-999" in [c.upper() for c in components]:
            errors.append(ValidationFailure(failure_type=ValidationFailureType.INVALID_SKU, message="Invalid SKU requested: 'BAD-SKU-999'"))
        
        # Missing categories check
        cats = [test_graph.graph.nodes[c].get("attr_component_category", "").upper() if c in test_graph.graph else "" for c in components]
        missing = []
        for mandatory in ["CPU", "MEMORY"]:
            if mandatory not in cats:
                missing.append(mandatory)
        if missing:
            errors.append(ValidationFailure(failure_type=ValidationFailureType.MISSING_REQUIRED_CATEGORY, message=f"Missing core categories: {','.join(missing)}"))
            
        is_valid = len(errors) == 0
        return is_valid, ["Mock validation run"], errors
    
    executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)

    # Disable LLM calls, strictly use heuristic fallback
    executor.generator.llm.select_components = MagicMock(return_value=([], [], []))

    # Execute query
    result = executor.execute_query("I need an AI server with BAD-SKU-999")
    
    ranked = result.get("ranked_solutions", [])
    assert len(ranked) == 3 # Cost, Balanced, Perf
    
    first_sol = ranked[0]
    # Delta should show BAD-SKU-999 was removed, and CPU/Memory added
    delta = first_sol.get("delta", {})
    assert "BAD-SKU-999" in delta.get("removed", [])
    
    # The heuristic should have picked up the missing categories
    components = first_sol.get("components", [])
    assert "hpe-proliant-dl380-gen12-processors-xeon-6505p" in components
    assert "hpe-proliant-dl380-gen12-components-6000mt" in components

def test_headless_neutral_scenario_missing_mandatory(test_graph):
    """Test providing a valid platform but missing CPU/Memory. Workflow should autofill."""
    executor = WorkflowExecutor(test_graph)
    
    req = CustomerRequest(
        request_id="test-2",
        workloads=["wl-ai"],
        requirements=[]
    )
    executor.parser.parse_request = MagicMock(return_value=req)
    
    from ikp_platform.core.ontology.models import ValidationFailure, ValidationFailureType

    def mock_evaluate(platform_id, components):
        errors = []
        cats = [test_graph.graph.nodes[c].get("attr_component_category", "").upper() if c in test_graph.graph else "" for c in components]
        missing = []
        for mandatory in ["CPU", "MEMORY"]:
            if mandatory not in cats:
                missing.append(mandatory)
        if missing:
            errors.append(ValidationFailure(failure_type=ValidationFailureType.MISSING_REQUIRED_CATEGORY, message=f"Missing core categories: {','.join(missing)}"))
            
        is_valid = len(errors) == 0
        return is_valid, ["Mock validation run"], errors
    
    executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)
    executor.generator.llm.select_components = MagicMock(return_value=([], [], []))

    result = executor.execute_query("I need an AI server")
    ranked = result.get("ranked_solutions", [])
    
    # Ensure it successfully found a valid solution by adding CPU and Memory
    first_sol = ranked[0]
    components = first_sol.get("components", [])
    assert "hpe-proliant-dl380-gen12-processors-xeon-6505p" in components
    assert "hpe-proliant-dl380-gen12-components-6000mt" in components
    
    delta = first_sol.get("delta", {})
    # Since original reqs was empty, added should contain CPU and Memory
    added = [c for c in delta.get("added", [])]
    assert "HPE-PROLIANT-DL380-GEN12-PROCESSORS-XEON-6505P" in added

def test_headless_positive_scenario(test_graph):
    """Test a fully correct offline BOQ."""
    executor = WorkflowExecutor(test_graph)
    
    req = CustomerRequest(
        request_id="test-3",
        workloads=["wl-ai"],
        requirements=[
            CustomerRequirement(category="technical", name="COMPONENT", value="hpe-proliant-dl380-gen12-processors-xeon-6505p"),
            CustomerRequirement(category="technical", name="COMPONENT", value="hpe-proliant-dl380-gen12-components-6000mt")
        ]
    )
    executor.parser.parse_request = MagicMock(return_value=req)
    
    def mock_evaluate(platform_id, components):
        return True, ["All good"], []
    
    executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)
    
    # Mock LLM to return exactly what was requested
    executor.generator.llm.select_components = MagicMock(return_value=(
        ["hpe-proliant-dl380-gen12-processors-xeon-6505p", "hpe-proliant-dl380-gen12-components-6000mt"],
        ["Picked correctly"],
        ["COMPONENT"]
    ))

    result = executor.execute_query("I need a complete AI server")
    ranked = result.get("ranked_solutions", [])
    first_sol = ranked[0]
    
    delta = first_sol.get("delta", {})
    assert len(delta.get("removed", [])) == 0 # Nothing removed
    
    # The platform id will be added because the LLM was only asked for components, 
    # and the generator prepends the platform. We ignore platform in SKU delta.
    assert "HPE-PROLIANT-DL380-GEN12" in delta.get("added", [])
