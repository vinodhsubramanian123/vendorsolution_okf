import pytest
from ikp_platform.core.ontology.models import CustomerRequest, Platform, Component, EngineeringObjectType
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.repository.graph_builder import GraphBuilder


def test_intent_parser():
    parser = IntentParser()
    request = parser.parse_request("I need an AI server with a GPU")
    
    assert "ai" in request.workloads
    assert any(req.value == "GPU" for req in request.requirements)


def test_solution_generator():
    graph = GraphBuilder()
    
    platform = Platform(id="test-platform", type=EngineeringObjectType.PLATFORM, title="Test Server")
    gpu = Component(
        id="test-gpu", 
        type=EngineeringObjectType.COMPONENT, 
        title="Test GPU", 
        component_category="GPU"
    )
    
    # Establish graph structure
    graph.add_concept(platform)
    graph.add_concept(gpu)
    
    # Manually add compatibility edge to simulate PDF extraction
    graph.graph.add_edge("test-gpu", "test-platform", relationship_type="Compatible With")
    
    generator = SolutionGenerator(graph)
    
    parser = IntentParser()
    request = parser.parse_request("I need a server with a GPU")
    
    candidates = generator.generate(request)
    
    assert len(candidates) > 0
    candidate = candidates[0]
    assert "test-platform" in candidate.components
    assert "test-gpu" in candidate.components
    assert candidate.validation_status == "Valid"


def test_rule_engine():
    graph = GraphBuilder()
    engine = RuleEngine(graph)
    
    platform = Platform(id="test-platform", type=EngineeringObjectType.PLATFORM, title="Test Server")
    gpu = Component(id="test-gpu", type=EngineeringObjectType.COMPONENT, title="Test GPU")
    
    graph.add_concept(platform)
    graph.add_concept(gpu)
    graph.graph.add_edge("test-gpu", "test-platform", relationship_type="Compatible With")
    
    is_valid, constraints_checked, rules_checked = engine.evaluate_solution("test-platform", ["test-gpu"])
    
    assert is_valid is True

def test_repo_graph_integration():
    from ikp_platform.core.repository.repo_manager import RepoManager
    import os
    repo = RepoManager("repository", str(os.getcwd()))
    repo.bootstrap()
    
    # Just checking it doesn't crash and we can query
    comp = repo.graph.get_compatible("dl380-gen12")
    assert comp is not None
