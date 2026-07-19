import pytest
import shutil

from ikp_platform.core.ontology.models import (
    Rule,
    RuleSeverity,
    ConfidenceLevel,
    EngineeringRelationship,
    RelationshipType,
)
from ikp_platform.core.repository.repo_manager import RepoManager


@pytest.fixture
def temp_repo_dir(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    yield repo_dir
    if repo_dir.exists():
        shutil.rmtree(repo_dir)


def test_okf_persistence_roundtrip(temp_repo_dir):
    """
    Test that relationships (edges) and body contents survive a restart/roundtrip.
    This validates the fix for Gap 0.1 where OKFReader dropped the markdown body.
    """
    # 1. Create initial state
    project_root = temp_repo_dir.parent
    manager1 = RepoManager(
        project_root=str(project_root), repository_path=str(temp_repo_dir)
    )

    # Create a rule with body sections and relationships
    test_rule = Rule(
        id="R-TEST-123",
        title="Test Rule",
        severity=RuleSeverity.ERROR,
        confidence=ConfidenceLevel.HIGH,
        expected_outcome="The system must function.",
        trigger_conditions=["Condition A", "Condition B"],
        relationships=[
            EngineeringRelationship(
                target_id="C-TEST-COMP", relationship_type=RelationshipType.REQUIRES
            )
        ],
    )

    # Add concept and write to disk using the manager
    manager1.add_concept(test_rule)
    manager1.writer.write_concept(test_rule)

    # Verify graph state in first manager
    stats1 = manager1.graph.get_stats()
    assert stats1["total_nodes"] == 2
    assert stats1["total_edges"] == 1

    # 2. Simulate restart: create a completely new manager against the same directory
    manager2 = RepoManager(
        project_root=str(project_root), repository_path=str(temp_repo_dir)
    )
    manager2.bootstrap()

    # 3. Verify graph state in second manager
    stats2 = manager2.graph.get_stats()
    assert stats2["total_nodes"] == 2, "Failed to load node after restart"
    assert stats2["total_edges"] == 1, (
        "Failed to load edges after restart - Gap 0.1 regex issue!"
    )
