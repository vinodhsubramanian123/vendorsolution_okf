import pytest
import tempfile
import shutil
from ikp_platform.core.repository.graph_builder import GraphBuilder

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
