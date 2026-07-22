from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum
import uuid
from datetime import datetime


class CorrectionType(str, Enum):
    ATTRIBUTE_FIX = "AttributeFix"
    COMPATIBILITY_FIX = "CompatibilityFix"
    RULE_FIX = "RuleFix"
    MISSING_COMPONENT = "MissingComponent"
    PRICING_UPDATE = "PricingUpdate"


class HumanFeedback(BaseModel):
    """
    Template for human-in-the-loop feedback.
    Used by Vendor Portal / Partners to submit corrections when the AI
    has extracted something incorrectly or hallucinated.

    Phase 6: Evidence-backed corrections become VALIDATED KnowledgeDeltas
    and are immediately applied after acceptance (no PENDING review queue needed
    since a human has already confirmed the source).
    """
    feedback_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    component_id: Optional[str] = Field(None, description="The ID of the component being corrected")
    platform_id: Optional[str] = Field(None, description="The platform ID, if applicable")
    correction_type: CorrectionType = Field(..., description="Type of correction")
    corrected_value: Any = Field(..., description="The corrected value, constraint, or attribute")
    field_name: Optional[str] = Field(None, description="The specific attribute field being fixed (e.g., 'max_memory')")
    evidence_source: str = Field(..., description="Source of truth (e.g., 'HPE QuickSpecs Page 42' or 'Partner Portal')")
    reviewer_notes: str = Field("", description="Additional notes from the human reviewer")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


def apply_feedback(feedback: HumanFeedback, repo_manager) -> None:
    """
    Translates a HumanFeedback submission into a KnowledgeDelta
    and applies it to the repository to update the Graph/Vector store.
    Uses DeltaChangeType.UPDATED_ATTRIBUTE for attribute fixes.
    """
    from ikp_platform.core.ontology.models import (
        KnowledgeDelta, DeltaChange, DeltaChangeType, DeltaStatus
    )

    # Pick the most appropriate change type based on correction_type
    change_type_map = {
        CorrectionType.ATTRIBUTE_FIX: DeltaChangeType.UPDATED_ATTRIBUTE,
        CorrectionType.COMPATIBILITY_FIX: DeltaChangeType.COMPATIBILITY_CHANGE,
        CorrectionType.RULE_FIX: DeltaChangeType.UPDATED_RULE,
        CorrectionType.MISSING_COMPONENT: DeltaChangeType.NEW_COMPONENT,
        CorrectionType.PRICING_UPDATE: DeltaChangeType.UPDATED_ATTRIBUTE,
    }
    delta_change_type = change_type_map.get(feedback.correction_type, DeltaChangeType.UPDATED_ATTRIBUTE)

    change = DeltaChange(
        object_id=feedback.component_id or feedback.platform_id or "global",
        change_type=delta_change_type,
        field_name=feedback.field_name,
        old_value=None,  # Looked up at apply time by learning engine
        new_value=feedback.corrected_value,
    )

    delta = KnowledgeDelta(
        delta_id=feedback.feedback_id,
        source_id=f"human_feedback|{feedback.evidence_source}",
        changes=[change],
        timestamp=datetime.utcnow(),
        status=DeltaStatus.VALIDATED,  # Human-confirmed, no extra review needed
        review_notes=f"[{feedback.correction_type.value}] {feedback.reviewer_notes}",
    )

    repo_manager._record_delta(delta)
