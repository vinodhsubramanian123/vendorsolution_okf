"""
Rebuilds the semantic (vector) search index from everything already in
repository/. Run this after ingest_catalog.py, or any time you want to
refresh the index without re-parsing PDFs.

Requires GEMINI_API_KEY to do anything useful -- without it, every
embedding call fails and this indexes 0 objects (loudly, via logging,
not silently).
"""

import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.repository.repo_manager import RepoManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reindex")


def main():
    project_root = Path(__file__).parent.parent.parent
    repo_dir = project_root / "repository"

    repo = RepoManager(str(repo_dir), str(project_root))
    repo.bootstrap()

    logger.info("Rebuilding vector index from repository/ ...")
    count = repo.reindex_vector_store()
    logger.info(f"Indexed {count} objects into the vector store.")
    if count == 0:
        logger.warning(
            "0 objects indexed -- check GEMINI_API_KEY is set. "
            "Semantic search will return no results until this succeeds."
        )


if __name__ == "__main__":
    main()
