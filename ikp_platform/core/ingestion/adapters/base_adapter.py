from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from ikp_platform.core.ontology.models import BaseEngineeringObject, Platform, DeltaChange

class BasePDFAdapter(ABC):
    """
    Base class for vendor-specific PDF extraction logic.
    """
    
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        """Returns True if this adapter can process the given PDF text."""
        pass

    @abstractmethod
    def extract_platform(self, text: str) -> Optional[Platform]:
        """Extract the main platform object from the text."""
        pass

    @abstractmethod
    def extract_components(self, text: str, platform: Platform, structured_components: List[dict]) -> Tuple[List[BaseEngineeringObject], List[DeltaChange]]:
        """Extract all related components, rules, and workloads from the text and tables."""
        pass
