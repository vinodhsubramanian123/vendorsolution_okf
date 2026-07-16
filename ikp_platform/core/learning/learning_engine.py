"""
Learning Engine — Merges Knowledge Deltas into the canonical repository.

Governs: Blueprint 02 §9 (Continuous Learning Lifecycle),
         Blueprint 06 §12 (Continuous Learning),
         Blueprint 07 §12 (Continuous Learning)

Learning SHALL improve knowledge while preserving history.
Only validated learning SHALL update canonical engineering knowledge.
"""

from typing import List, Optional
from datetime import datetime
import logging

from ikp_platform.core.ontology.models import (
    KnowledgeDelta,
    DeltaStatus,
    DeltaChange,
    DeltaChangeType,
    BaseEngineeringObject,
    HistoryEntry,
)
from ikp_platform.core.repository.repo_manager import RepoManager

logger = logging.getLogger("ikp.learning")


class LearningEngine:
    """
    Accepts Knowledge Deltas from any source and merges validated changes
    into the canonical knowledge repository.

    Learning sources (Blueprint 06 §12):
    - Vendor Documents
    - Vendor Portals
    - Customer BOQs
    - Successful Configurations
    - Failed Configurations
    - Portal Validation
    - Support Cases
    - Human Decisions
    - Repository History
    - Engineering Corrections
    """

    def __init__(self, repo_manager: RepoManager):
        self.repo_manager = repo_manager
        self.pending_deltas: List[KnowledgeDelta] = []

    def submit_delta(self, delta: KnowledgeDelta) -> None:
        """
        Submit a Knowledge Delta for review.
        Deltas with sufficient confidence may be auto-approved.
        Otherwise they are queued for human review.
        """
        # Auto-approve deltas from high-confidence sources
        if self._can_auto_approve(delta):
            delta.status = DeltaStatus.VALIDATED
            logger.info(f"Auto-approved delta {delta.delta_id} from {delta.source_id}")
        else:
            delta.status = DeltaStatus.NEEDS_REVIEW
            logger.info(f"Delta {delta.delta_id} queued for human review")

        self.pending_deltas.append(delta)

    def process_validated_deltas(self, objects: List[BaseEngineeringObject]) -> int:
        """
        Merge all validated deltas into the canonical repository.
        Returns the number of deltas merged.

        Blueprint 06 §7: Never overwrite evidence. Never overwrite history.
        """
        merged_count = 0

        for delta in self.pending_deltas:
            if delta.status == DeltaStatus.VALIDATED:
                # Find objects that belong to this delta
                delta_objects = [
                    obj for obj in objects
                    if any(c.object_id == obj.id for c in delta.changes)
                ]

                if delta_objects:
                    self.repo_manager.apply_delta(delta, delta_objects)
                    merged_count += 1
                    logger.info(
                        f"Merged delta {delta.delta_id}: "
                        f"{len(delta.changes)} changes, "
                        f"{len(delta_objects)} objects"
                    )

        # Remove merged deltas from pending
        self.pending_deltas = [
            d for d in self.pending_deltas
            if d.status != DeltaStatus.MERGED
        ]

        return merged_count

    def approve_delta(self, delta_id: str, reviewer: str, notes: Optional[str] = None) -> bool:
        """
        Human approves a pending delta.
        Blueprint 02 §10: Approved decisions become future engineering knowledge.
        """
        for delta in self.pending_deltas:
            if delta.delta_id == delta_id:
                delta.status = DeltaStatus.VALIDATED
                delta.reviewed_by = reviewer
                delta.review_notes = notes
                logger.info(f"Delta {delta_id} approved by {reviewer}")
                return True
        return False

    def reject_delta(self, delta_id: str, reviewer: str, reason: str) -> bool:
        """Reject a pending delta with a reason."""
        for delta in self.pending_deltas:
            if delta.delta_id == delta_id:
                delta.status = DeltaStatus.REJECTED
                delta.reviewed_by = reviewer
                delta.review_notes = reason
                logger.info(f"Delta {delta_id} rejected by {reviewer}: {reason}")
                return True
        return False

    def get_pending_reviews(self) -> List[KnowledgeDelta]:
        """Get all deltas awaiting human review."""
        return [
            d for d in self.pending_deltas
            if d.status == DeltaStatus.NEEDS_REVIEW
        ]

    @staticmethod
    def _can_auto_approve(delta: KnowledgeDelta) -> bool:
        """
        Determine if a delta can be auto-approved based on confidence.
        Conservative policy: only auto-approve if ALL changes have high-confidence evidence.
        """
        if not delta.changes:
            return False

        for change in delta.changes:
            if change.evidence and change.evidence.confidence.value != "High":
                return False
            if not change.evidence:
                return False

        return True
