from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ikp_platform.core.ontology.models import ValidationFailure
from ikp_platform.core.validation.validator import ValidationMessage

class ValidationContext(BaseModel):
    """
    State object passed between independent validation plugins.
    """
    platform_id: Optional[str] = None
    original_components: List[str] = Field(default_factory=list)
    corrected_components: List[str] = Field(default_factory=list)
    
    is_valid: bool = True
    messages: List[ValidationMessage] = Field(default_factory=list)
    errors: List[ValidationFailure] = Field(default_factory=list)
    reasoning_chain: List[str] = Field(default_factory=list)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ValidationStep(ABC):
    """
    Abstract interface for a plugin in the Validation Pipeline.
    """
    @abstractmethod
    def execute(self, context: ValidationContext) -> ValidationContext:
        """
        Takes the current context, applies its domain logic, and returns the modified context.
        """
        pass

class ValidationPipeline:
    """
    Orchestrates a series of independent ValidationSteps.
    """
    def __init__(self, steps: List[ValidationStep]):
        self.steps = steps

    def execute(self, initial_context: ValidationContext) -> ValidationContext:
        context = initial_context
        for step in self.steps:
            context = step.execute(context)
        return context
