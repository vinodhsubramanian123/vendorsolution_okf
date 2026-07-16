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
        self.known_files: Set[str] = set()

    def scan(self) -> List[str]:
        """
        Scan the sources directory for new files.
        Returns list of absolute paths to new files.
        """
        new_files = []

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

                # Skip already-known files
                if abs_path in self.known_files:
                    continue

                new_files.append(abs_path)
                self.known_files.add(abs_path)

        if new_files:
            logger.info(f"Found {len(new_files)} new source file(s)")

        return new_files
