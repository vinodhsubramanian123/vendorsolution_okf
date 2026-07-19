from ikp_platform.core.ontology.models import Platform, Component, EngineeringObjectType
from ikp_platform.core.reasoning.intent_parser import IntentParser
from ikp_platform.core.reasoning.rule_engine import RuleEngine
from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
from ikp_platform.core.repository.graph_builder import GraphBuilder

from unittest.mock import patch, MagicMock

@patch("ikp_platform.core.reasoning.intent_parser.LLMClient.parse_intent")
def test_intent_parser(mock_parse_intent):
    mock_parse_intent.return_value = {
        "workloads": ["ai"],
        "requirements": [{"category": "technical", "name": "Accelerator", "value": "GPU"}],
        "vendor_preference": None
    }
    parser = IntentParser()
    request = parser.parse_request("I need an AI server with a GPU")

    assert "ai" in request.workloads
    assert any(req.value == "GPU" for req in request.requirements)


@patch("ikp_platform.core.reasoning.intent_parser.LLMClient.parse_intent")
def test_solution_generator(mock_parse_intent):
    mock_parse_intent.return_value = {
        "workloads": ["ai"],
        "requirements": [{"category": "technical", "name": "Accelerator", "value": "GPU"}],
        "vendor_preference": None
    }
    graph = GraphBuilder()

    platform = Platform(
        id="test-platform", type=EngineeringObjectType.PLATFORM, title="Test Server", capabilities=["ai"]
    )
    gpu = Component(
        id="test-gpu",
        type=EngineeringObjectType.COMPONENT,
        title="Test GPU",
        component_category="GPU",
    )

    # Establish graph structure
    graph.add_concept(platform)
    graph.add_concept(gpu)

    # Manually add compatibility edge to simulate PDF extraction
    graph.graph.add_edge(
        "test-gpu", "test-platform", relationship_type="Compatible With"
    )

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

    platform = Platform(
        id="test-platform", type=EngineeringObjectType.PLATFORM, title="Test Server"
    )
    gpu = Component(
        id="test-gpu", type=EngineeringObjectType.COMPONENT, title="Test GPU"
    )

    graph.add_concept(platform)
    graph.add_concept(gpu)
    graph.graph.add_edge(
        "test-gpu", "test-platform", relationship_type="Compatible With"
    )

    is_valid, constraints_checked, rules_checked = engine.evaluate_solution(
        "test-platform", ["test-gpu"]
    )

    assert is_valid is True


def test_repo_graph_integration(temp_repo):
    # temp_repo (see conftest.py) is rooted under pytest's tmp_path and
    # seeded with fixture data -- this must never point at the real,
    # on-disk project repository/, or it silently overwrites the real
    # STATE.md as a side effect of running the test suite. (This has
    # regressed back to a hardcoded os.getcwd() RepoManager call twice
    # now -- if you're reading this because it happened a third time,
    # grep the whole tests/ tree for RepoManager( before assuming this
    # fixture is the problem.)
    comp = temp_repo.graph.get_compatible("fixture-dl380-gen12")
    assert comp is not None
    assert "fixture-dl380-gen12/gpu/nvidia-h100" in comp
