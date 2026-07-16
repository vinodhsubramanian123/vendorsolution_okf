"""
Source Registry — Registers, classifies, and tracks engineering sources.

Governs: Blueprint 04 §5 (Source Registration), Blueprint 07 §3

Every source receives a permanent identity. The original source is preserved.
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import logging

from ikp_platform.core.ontology.models import (
    Source,
    SourceType,
    ProcessingStatus,
    ConfidenceLevel,
)

logger = logging.getLogger("ikp.ingestion")

# Map file extensions to source types
EXTENSION_MAP = {
    ".pdf": SourceType.PDF,
    ".xlsx": SourceType.EXCEL,
    ".xls": SourceType.EXCEL,
    ".csv": SourceType.CSV,
    ".json": SourceType.JSON,
    ".xml": SourceType.XML,
}


class SourceRegistry:
    """
    Registers and classifies engineering sources.
    Blueprint 04 §5: Every source SHALL receive a permanent identity.
    """

    def __init__(self):
        self.sources: List[Source] = []

    def register(self, file_path: str) -> Source:
        """
        Register a new engineering source file.
        Assigns permanent identity, classifies type, computes hash.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Source not found: {file_path}")

        # Classify source type from extension
        source_type = EXTENSION_MAP.get(path.suffix.lower())
        if source_type is None:
            source_type = SourceType.PDF  # Default fallback

        # Compute file hash for duplicate detection
        file_hash = self._compute_hash(path)

        # Check for duplicates
        for existing in self.sources:
            if existing.file_hash == file_hash:
                logger.warning(f"Duplicate source detected: {file_path} matches {existing.source_id}")
                return existing

        # Infer metadata from filename
        title = path.stem
        vendor = self._infer_vendor(title)

        source = Source(
            source_type=source_type,
            vendor=vendor,
            original_file_path=str(path.absolute()),
            processing_status=ProcessingStatus.REGISTERED,
            title=title,
            file_hash=file_hash,
            confidence=ConfidenceLevel.UNVERIFIED,
        )

        self.sources.append(source)
        logger.info(f"Registered source {source.source_id}: {title} ({source_type.value})")
        return source

    def update_status(self, source_id: str, status: ProcessingStatus) -> None:
        """Update the processing status of a source."""
        for source in self.sources:
            if source.source_id == source_id:
                source.processing_status = status
                return

    @staticmethod
    def _compute_hash(path: Path) -> str:
        """Compute SHA-256 hash of a file for duplicate detection."""
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()[:16]

    @staticmethod
    def _infer_vendor(filename: str) -> Optional[str]:
        """Attempt to infer vendor from filename."""
        vendors = {
            "hpe": "HPE",
            "dell": "Dell",
            "lenovo": "Lenovo",
            "cisco": "Cisco",
            "netapp": "NetApp",
            "pure": "Pure Storage",
            "nutanix": "Nutanix",
        }
        lower = filename.lower()
        for key, vendor in vendors.items():
            if key in lower:
                return vendor
        return None
