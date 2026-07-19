import pytest
from unittest.mock import MagicMock
from ikp_platform.core.workflow.executor import WorkflowExecutor
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import Platform, Workload, EngineeringRelationship, RelationshipType
from ikp_platform.core.ontology.models import CustomerRequest, CustomerRequirement, SolutionCandidate, ConfidenceLevel

@pytest.fixture
def mock_graph():
    """Create a minimal mocked Knowledge Graph for testing the workflow."""
    graph = GraphBuilder()
    
    # Add Workload
    wl = Workload(
        id="workload-ai-and-machine-learning",
        title="AI/ML",
        description="AI/ML Workload",
        vendor="Generic",
        solution_domain="Compute"
    )
    graph.add_concept(wl)
    
    # Add Platform
    plat = Platform(
        id="dl380",
        title="ProLiant DL380",
        description="2U Server",
        vendor="HPE",
        solution_domain="Compute",
        relationships=[
            EngineeringRelationship(
                target_id="workload-ai-and-machine-learning",
                relationship_type=RelationshipType.SUPPORTS
            )
        ]
    )
    graph.add_concept(plat)
    
    # Add Component
    from ikp_platform.core.ontology.models import Component
    comp = Component(
        id="cpu-1",
        title="Intel CPU",
        description="CPU",
        vendor="Intel",
        solution_domain="Compute",
        component_category="CPU",
        relationships=[
            EngineeringRelationship(
                target_id="dl380",
                relationship_type=RelationshipType.COMPATIBLE_WITH
            )
        ]
    )
    graph.add_concept(comp)
    
    # Mock rule engine to always say valid for the test
    graph.rule_engine = MagicMock()
    graph.rule_engine.evaluate_solution.return_value = (True, [], [])
    
    return graph


def test_workflow_execution(mock_graph):
    """Test the LangGraph pipeline from intent to ranked solutions."""
    executor = WorkflowExecutor(mock_graph)
    
    # Mock parser and generator to avoid real LLM calls and infinite loops
    executor.parser.parse_request = MagicMock()
    req = CustomerRequest(request_id="req-1", workloads=["workload-ai-and-machine-learning"])
    executor.parser.parse_request.return_value = req
    
    executor.generator.generate = MagicMock()
    candidate = SolutionCandidate(
        request_id="req-1",
        profile="Balanced",
        components=["dl380", "cpu-1"],
        reasoning_chain=["mocked"],
        requirements_satisfied=[],
        confidence=ConfidenceLevel.HIGH,
        validation_status="Valid"
    )
    executor.generator.generate.return_value = [candidate]
    
    result = executor.execute_query("I need an AI server")
    
    assert "platform" in result
    assert "bom" in result
    assert "ranked_solutions" in result
    
    ranked = result["ranked_solutions"]
    assert len(ranked) == 1
    assert ranked[0]["profile"] == "Balanced"
