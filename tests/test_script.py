import sys
sys.path.append(".")
from ikp_platform.core.repository.repo_manager import RepoManager
repo = RepoManager("/home/vinodh/vendorsolution_okf/repository", ".")
repo.bootstrap()
platforms = repo.graph.filter_by_type("Platform")
print("Platforms:", platforms)
for pid in platforms:
    print(pid)
    print("  title:", repo.graph.graph.nodes[pid].get("title"))
    print("  description:", repo.graph.graph.nodes[pid].get("description")[:100] if repo.graph.graph.nodes[pid].get("description") else None)
