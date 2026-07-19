import pytest
from unittest.mock import MagicMock, patch
from ikp_platform.core.workflow.executor import WorkflowExecutor
from ikp_platform.core.ontology.models import (
    CustomerRequest, CustomerRequirement, ValidationFailure, ValidationFailureType,
    Platform, Component, EngineeringRelationship, RelationshipType
)
from ikp_platform.core.repository.graph_builder import GraphBuilder

@pytest.fixture
def test_graph():
    graph = GraphBuilder()
    
    # Platform
    plat = Platform(
        id="PLATFORM-1",
        title="Test Platform",
        capabilities=["wl-ai"]
    )
    graph.add_concept(plat)
    
    # Component
    comp = Component(
        id="COMP-RAM-16GB",
        title="16GB RAM",
        component_category="MEMORY",
        relationships=[EngineeringRelationship(target_id="PLATFORM-1", relationship_type=RelationshipType.COMPATIBLE_WITH)]
    )
    graph.add_concept(comp)
    
    return graph

def test_infinite_oscillation_prevention(test_graph):
    """Test that if the rule engine forces an infinite loop, the orchestrator detects the cycle and exits to HITL."""
    executor = WorkflowExecutor(test_graph)

    req = CustomerRequest(
        request_id="test-cycle",
        workloads=["wl-ai"],
        requirements=[
            CustomerRequirement(category="technical", name="RAM", value="16GB")
        ]
    )

    from ikp_platform.core.workflow.nodes import WorkflowNodes
    with patch.object(WorkflowNodes, "draft_bom") as mock_draft:
        def _mock_draft_fn(*args, **kwargs):
            state = args[0] if args else kwargs.get("state", {})
            return {
                "current_bom": ["PLATFORM-1", "COMP-RAM-16GB"],
                "ranked_solutions": [],
                "attempt_count": state.get("attempt_count", 0) + 1,
                "needs_regeneration": False
            }
        mock_draft.side_effect = _mock_draft_fn

        with patch.object(WorkflowNodes, "select_recovery_strategy") as mock_recov:
            mock_recov.side_effect = lambda *args, **kwargs: {"needs_regeneration": False}

            executor = WorkflowExecutor(test_graph)
            executor.parser.parse_request = MagicMock(return_value=req)

            def mock_evaluate(platform_id, components):
                errors = [ValidationFailure(
                    failure_type=ValidationFailureType.INCOMPATIBLE,
                    message="Cyclic missing dependency",
                    object_id="COMP-RAM-16GB"
                )]
                return False, ["Mock validation run"], errors

            executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)
            result = executor.execute_query("Give me a server with 16GB RAM")

    # It should have caught the cycle and triggered human intervention
    assert result.get("requires_human_intervention") is True

    payload = result.get("human_review_payload", {})
    assert payload.get("cycle_detected") is True
    assert len(result.get("visited_bom_hashes", [])) == 1

def test_exhaustion_limits(test_graph):
    """Test that the orchestrator respects max_attempts (3) when failures are unique (no cycles)."""
    req = CustomerRequest(
        request_id="test-limit",
        workloads=["wl-ai"],
        requirements=[
            CustomerRequirement(category="technical", name="RAM", value="16GB")
        ]
    )
    
    from ikp_platform.core.reasoning.solution_generator import SolutionGenerator
    
    call_count = [0]
    def mock_generate(self, request):
        call_count[0] += 1
        print(f"DEBUG: mock_generate called, count={call_count[0]}")
        from ikp_platform.core.ontology.models import SolutionCandidate, ConfidenceLevel
        return [SolutionCandidate(
            request_id="test-limit",
            profile="Cost",
            components=["PLATFORM-1", f"COMP-UNIQUE-{call_count[0]}"],
            confidence=ConfidenceLevel.LOW,
            validation_status="Pending"
        )]

    with patch.object(SolutionGenerator, "generate", new=mock_generate):
        executor = WorkflowExecutor(test_graph)
        executor.parser.parse_request = MagicMock(return_value=req)

        def mock_evaluate(platform_id, components):
            print(f"DEBUG: mock_evaluate called with {components}")
            errors = [ValidationFailure(
                failure_type=ValidationFailureType.INCOMPATIBLE,
                message=f"Missing dependency for {components[1]}",
                object_id=components[1]
            )]
            return False, ["Mock validation run"], errors

        executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)
        
        # Print state changes during test
        orig_invoke = executor.app.invoke
        def debug_invoke(state):
            print(f"DEBUG: initial invoke")
            return orig_invoke(state)
        executor.app.invoke = debug_invoke

        result = executor.execute_query("Test exhaustion")
        print(f"DEBUG: Final result attempt_count={result.get('attempt_count')} cycle={result.get('cycle_detected')}")

        assert result.get("requires_human_intervention") is True
        assert result.get("attempt_count") == 3
        assert result.get("cycle_detected") is False
        assert len(result.get("visited_bom_hashes", [])) == 3
