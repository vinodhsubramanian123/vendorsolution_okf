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

@pytest.fixture
def test_graph():
    """Create a graph for chaos testing."""
    graph = GraphBuilder()

    # Workload
    wl = Workload(id="wl-chaos", title="Chaos Workload", solution_domain="Compute")
    graph.add_concept(wl)

    # Platform
    plat = Platform(
        id="chaos-platform-1",
        title="Chaos Server",
        capabilities=["wl-chaos"],
        mandatory_categories=["CPU"],
        relationships=[EngineeringRelationship(target_id="wl-chaos", relationship_type=RelationshipType.SUPPORTS)]
    )
    graph.add_concept(plat)

    # CPU
    cpu = Component(
        id="chaos-cpu-1",
        title="Chaos CPU",
        component_category="CPU",
        relationships=[EngineeringRelationship(target_id="chaos-platform-1", relationship_type=RelationshipType.COMPATIBLE_WITH)]
    )
    graph.add_concept(cpu)

    return graph

def test_llm_complete_outage_fallback(test_graph):
    """
    Test what happens if the LLM completely fails (e.g. 503 or 429) during the workflow.
    The orchestrator should NOT crash. It should fall back to the heuristic logic and still output a valid BOQ.
    """
    executor = WorkflowExecutor(test_graph)
    
    # We simulate parse_intent failing or being hardcoded.
    req = CustomerRequest(
        request_id="chaos-1",
        workloads=["wl-chaos"],
        requirements=[
            CustomerRequirement(category="technical", name="CPU", value="Any")
        ]
    )
    executor.parser.parse_request = MagicMock(return_value=req)
    
    # Simulate LLMClient raising an exception (e.g. google.genai.errors.APIError)
    # The SolutionGenerator wraps this in try/except or the node handles it.
    # Actually, SolutionGenerator handles generating candidates. If LLM raises, it returns empty lists.
    # Let's mock the internal llm client to raise an exception.
    executor.generator.llm.select_components = MagicMock(side_effect=Exception("503 Service Unavailable"))
    
    # Run the query
    result = executor.execute_query("I need a chaos server with any cpu")
    
    # It should not crash. It should have ranked solutions using the fallback mechanism.
    ranked = result.get("ranked_solutions", [])
    assert len(ranked) > 0, "No solutions were generated during an LLM outage."
    
    first_sol = ranked[0]
    components = first_sol.get("components", [])
    
    # Fallback should have found the chaos-cpu-1
    assert "chaos-platform-1" in components
    assert "chaos-cpu-1" in components
