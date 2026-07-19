import time
import threading
import logging
from pathlib import Path
from typing import Dict

from ikp_platform.core.repository.repo_manager import RepoManager

logger = logging.getLogger("ikp.repository.watcher")

class RepositoryWatcher:
    """
    Background watcher that monitors the repository/ directory for external edits
    (e.g., a human editing markdown files directly in Obsidian).
    When edits are detected via mtime changes, it syncs the in-memory graph
    and the vector store.
    """

    def __init__(self, repo_manager: RepoManager, scan_interval: int = 5):
        self.repo = repo_manager
        self.scan_interval = scan_interval
        self._mtime_cache: Dict[str, float] = {}
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._watch_loop, daemon=True, name="RepoWatcherThread")
            self._thread.start()
            logger.info("RepositoryWatcher started.")

    def stop(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=2.0)
            logger.info("RepositoryWatcher stopped.")

    def _watch_loop(self):
        # Initialize baseline without triggering updates
        self._scan_and_update(baseline_only=True)

        while not self._stop_event.is_set():
            time.sleep(self.scan_interval)
            try:
                self._scan_and_update(baseline_only=False)
            except Exception as e:
                logger.error(f"Error in RepositoryWatcher loop: {e}", exc_info=True)

    def _scan_and_update(self, baseline_only: bool = False):
        if not self.repo.repository_path.exists():
            return

        updated_files = []
        for root, _, files in self.repo.repository_path.walk() if hasattr(self.repo.repository_path, "walk") else self._fallback_walk(self.repo.repository_path):
            for file in files:
                if not file.endswith(".md"):
                    continue
                
                # Ignore metadata files
                if file in ["index.md", "LOG.md", "STATE.md", "CONTEXT.md"]:
                    continue

                full_path = Path(root) / file
                try:
                    mtime = full_path.stat().st_mtime
                    abs_path = str(full_path.absolute())
                    
                    if abs_path not in self._mtime_cache:
                        self._mtime_cache[abs_path] = mtime
                        if not baseline_only:
                            updated_files.append(full_path)
                    elif mtime > self._mtime_cache[abs_path]:
                        self._mtime_cache[abs_path] = mtime
                        if not baseline_only:
                            updated_files.append(full_path)
                except FileNotFoundError:
                    pass

        if updated_files and not baseline_only:
            logger.info(f"Detected {len(updated_files)} externally modified OKF file(s). Syncing graph and vectors...")
            objects_to_reindex = []
            for filepath in updated_files:
                try:
                    # Parse directly to get the objects
                    objs = self.repo.reader._parse_file(filepath)
                    for obj in objs:
                        self.repo.graph.add_concept(obj)
                        objects_to_reindex.append(obj)
                        logger.info(f"Synced {obj.type.value}: {obj.id}")
                except Exception as e:
                    logger.warning(f"Failed to sync {filepath}: {e}")

            if objects_to_reindex:
                # Update vector store
                self.repo.vector_store.index_many(objects_to_reindex, batch_size=20)
                logger.info("Successfully re-indexed modified files into the vector store.")

    def _fallback_walk(self, path: Path):
        import os
        for root, dirs, files in os.walk(path):
            yield root, dirs, files
