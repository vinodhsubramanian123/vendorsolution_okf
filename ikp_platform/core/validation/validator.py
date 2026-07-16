"""
Vendor Validation — Abstract interface for vendor validation integration.

Governs: Blueprint 02 §8 (Validation Lifecycle), Blueprint 05 §12 (Vendor Validation),
         Blueprint 06 §8 (Validation Strategy), Blueprint 07 §8 (Vendor Validation)

Every validation result produces a Knowledge Delta that feeds back into the
Learning Loop. In V1.0, this starts as a manual human review mode with a
clear interface for future portal API integration.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from ikp_platform.core.ontology.models import (
    KnowledgeDelta,
    DeltaChange,
    DeltaChangeType,
    EvidenceRecord,
    ConfidenceLevel,
)
import uuid


# ---------------------------------------------------------------------------
# Validation Result Models
# ---------------------------------------------------------------------------

class ValidationMessage(BaseModel):
    """A single message from a validation check."""
    severity: str  # "Error", "Warning", "Info", "Recommendation"
    code: Optional[str] = None
    message: str
    affected_object: Optional[str] = None
    recommended_action: Optional[str] = None


class ValidationResult(BaseModel):
    """
    Complete result of validating a solution candidate.
    Blueprint 06 §9: Portal advice SHALL be treated as engineering evidence.
    """
    validation_id: str = Field(default_factory=lambda: f"VAL-{str(uuid.uuid4())[:8]}")
    solution_id: str
    validator_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_valid: bool = False
    messages: List[ValidationMessage] = []
    configuration_errors: List[str] = []
    missing_components: List[str] = []
    dependency_violations: List[str] = []
    compatibility_issues: List[str] = []
    licensing_issues: List[str] = []
    firmware_issues: List[str] = []
    portal_recommendations: List[str] = []


# ---------------------------------------------------------------------------
# Abstract Validator
# ---------------------------------------------------------------------------

class VendorValidator(ABC):
    """
    Abstract base class for vendor validation.
    Subclass this for each vendor portal integration.
    """

    @abstractmethod
    def validate(self, solution_components: List[str], context: dict) -> ValidationResult:
        """
        Validate a solution against vendor systems.

        Args:
            solution_components: List of engineering object IDs in the solution.
            context: Additional context (vendor, platform, etc.).

        Returns:
            ValidationResult with all findings.
        """
        pass

    def to_knowledge_delta(self, result: ValidationResult) -> KnowledgeDelta:
        """
        Convert a ValidationResult into a Knowledge Delta.
        Blueprint 05 §12: Validation feedback SHALL become Knowledge Delta.
        """
        changes = []

        for msg in result.messages:
            if msg.severity in ("Error", "Warning"):
                changes.append(DeltaChange(
                    change_type=DeltaChangeType.NEW_RULE,
                    object_id=msg.affected_object or result.solution_id,
                    field_name=f"validation_{msg.severity.lower()}",
                    new_value=msg.message,
                    evidence=EvidenceRecord(
                        source_id=result.validator_name,
                        confidence=ConfidenceLevel.HIGH,
                        description=f"Vendor validation: {msg.message}",
                    ),
                ))

        return KnowledgeDelta(
            source_id=f"validation:{result.validator_name}",
            changes=changes,
        )


# ---------------------------------------------------------------------------
# Manual Review Validator (V1.0 default)
# ---------------------------------------------------------------------------

class ManualReviewValidator(VendorValidator):
    """
    V1.0 implementation: flags solutions for human engineering review.
    Blueprint 02 §10: Human engineers remain responsible for engineering judgment.
    """

    def validate(self, solution_components: List[str], context: dict) -> ValidationResult:
        return ValidationResult(
            solution_id=context.get("solution_id", "unknown"),
            validator_name="ManualReview",
            is_valid=False,  # Requires human approval
            messages=[
                ValidationMessage(
                    severity="Info",
                    message="Solution requires human engineering review before deployment.",
                    recommended_action="Review solution components and approve or reject.",
                )
            ],
        )
