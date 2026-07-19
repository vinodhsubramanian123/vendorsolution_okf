import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
from ikp_platform.core.repository.repo_manager import RepoManager  # noqa: E402

repo = RepoManager(str(PROJECT_ROOT / "repository"), str(PROJECT_ROOT))
repo.bootstrap()
platforms = repo.graph.filter_by_type("Platform")
print("Platforms:", platforms)
for pid in platforms:
    print(pid)
    print("  title:", repo.graph.graph.nodes[pid].get("title"))
    print(
        "  description:",
        repo.graph.graph.nodes[pid].get("description")[:100]
        if repo.graph.graph.nodes[pid].get("description")
        else None,
    )
