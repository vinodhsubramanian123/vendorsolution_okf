"""
Shared pytest fixtures.

CRITICAL: tests must never point a RepoManager at the real project's
`repository/` folder or write to the real `STATE.md` / `LOG.md` /
`CONTEXT.md`. Every fixture here that touches RepoManager is rooted
under `tmp_path` so running the test suite is side-effect free against
the checked-out repo. This has broken twice already (once via a
hardcoded `os.getcwd()` in a test, once via `test_api_endpoints.py`
importing `api.app` directly) -- if you're adding a new test that
touches RepoManager, use `temp_repo` / `api_client` below rather than
pointing at PROJECT_ROOT or the real repository/ directory.
"""
import pytest
import tempfile
import shutil

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.repository.repo_manager import RepoManager
from ikp_platform.core.ontology.models import (
    Platform,
    Component,
    EvidenceRecord,
    EngineeringRelationship,
    RelationshipType,
    ConfidenceLevel,
    PackagingType,
)


@pytest.fixture
def shared_temp_dir():
    """Create a shared temporary directory for test artifacts."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


@pytest.fixture
def empty_graph():
    """Returns a clean GraphBuilder instance."""
    return GraphBuilder()


@pytest.fixture
def temp_repo(tmp_path):
    """A RepoManager fully isolated in a pytest tmp_path, seeded with a
    minimal but realistic platform + component so reasoning/query tests
    have something real to match against without needing live PDFs,
    a live LLM key, or the real on-disk repository/."""
    repo_dir = tmp_path / "repository"
    project_root = tmp_path

    repo = RepoManager(str(repo_dir), str(project_root))

    evidence = [EvidenceRecord(source_id="test_fixture", confidence=ConfidenceLevel.HIGH)]

    gpu = Component(
        id="fixture-dl380-gen12/gpu/nvidia-h100",
        title="NVIDIA H100 GPU",
        vendor="NVIDIA",
        component_category="GPU",
        packaging_type=PackagingType.STANDALONE,
        capabilities=["ai", "gpu"],
        tags=["ai", "gpu", "nvme"],
        evidence=evidence,
    )

    platform = Platform(
        id="fixture-dl380-gen12",
        title="HPE ProLiant DL380 Gen12 (fixture)",
        vendor="HPE",
        solution_domain="Compute",
        product_family="ProLiant",
        generation="Gen12",
        capabilities=["ai", "virtualization"],
        tags=["ai", "gpu", "nvme"],
        evidence=evidence,
        relationships=[
            EngineeringRelationship(
                target_id=gpu.id,
                relationship_type=RelationshipType.COMPATIBLE_WITH,
                evidence=evidence,
            )
        ],
    )

    repo.add_concept(gpu)
    repo.add_concept(platform)

    return repo


@pytest.fixture
def api_client(temp_repo, monkeypatch):
    """A FastAPI TestClient wired to `temp_repo` instead of the real,
    on-disk project repository. Clears api.get_repo's lru_cache before
    patching so no state leaks between tests."""
    from fastapi.testclient import TestClient
    from ikp_platform import api as api_module

    api_module.get_repo.cache_clear()
    monkeypatch.setattr(api_module, "get_repo", lambda: temp_repo)

    client = TestClient(api_module.app)
    yield client
    # No teardown call to get_repo.cache_clear() here: monkeypatch
    # restores the original get_repo automatically at fixture teardown,
    # and its cache is cleared at the top of this fixture on the next
    # test, before it's ever called again.
