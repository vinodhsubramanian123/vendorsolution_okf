from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
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
    Used by the Vendor Portal / Partners to submit corrections when the AI
    has extracted something incorrectly or hallucinated.
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
    """
    from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaChange, ChangeType, DeltaStatus
    
    change = DeltaChange(
        object_id=feedback.component_id or feedback.platform_id or "global",
        change_type=ChangeType.MODIFY if feedback.component_id else ChangeType.ADD,
        field_name=feedback.field_name,
        old_value=None, # To be looked up
        new_value=feedback.corrected_value,
        reason=f"Human Feedback ({feedback.correction_type.value}): {feedback.reviewer_notes}"
    )
    
    delta = KnowledgeDelta(
        delta_id=feedback.feedback_id,
        source_id=f"human_feedback_{feedback.evidence_source}",
        changes=[change],
        timestamp=datetime.utcnow(),
        status=DeltaStatus.VALIDATED, # Auto-validated since it's human feedback
        review_notes=feedback.reviewer_notes
    )
    
    repo_manager._record_delta(delta)
