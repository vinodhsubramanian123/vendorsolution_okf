"""
Source Watcher — Detects new engineering sources in the sources/ directory.

Governs: Blueprint 04 §4, Blueprint 07 §3, Implementation Checklist item 2
"""

import os
from pathlib import Path
from typing import List, Set
import logging

logger = logging.getLogger("ikp.ingestion")

SUPPORTED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".csv", ".json", ".xml"}


class SourceWatcher:
    """
    Monitors the sources/ directory tree for new or changed files.
    Maintains a set of already-seen file hashes to avoid re-processing.
    """

    def __init__(self, sources_path: str):
        self.sources_path = Path(sources_path)
        self.state_file = self.sources_path / ".watcher_state.json"
        self.known_files: dict[str, float] = {}
        self._load_state()

    def _load_state(self):
        import json
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    self.known_files = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load watcher state: {e}")

    def _save_state(self):
        import json
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.known_files, f)
        except Exception as e:
            logger.error(f"Failed to save watcher state: {e}")

    def scan(self) -> List[str]:
        """
        Scan the sources directory for new files.
        Returns list of absolute paths to new files.
        """
        new_files: List[str] = []

        if not self.sources_path.exists():
            logger.warning(f"Sources directory does not exist: {self.sources_path}")
            return new_files

        for root, dirs, files in os.walk(self.sources_path):
            for filename in files:
                file_path = Path(root) / filename
                abs_path = str(file_path.absolute())

                # Skip unsupported extensions
                if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                try:
                    mtime = os.path.getmtime(file_path)
                except OSError:
                    continue

                # Skip already-known files that haven't been modified
                if abs_path in self.known_files and self.known_files[abs_path] == mtime:
                    continue

                new_files.append(abs_path)
                self.known_files[abs_path] = mtime

        if new_files:
            logger.info(f"Found {len(new_files)} new/modified source file(s)")
            self._save_state()

        return new_files
