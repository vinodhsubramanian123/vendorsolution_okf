import hashlib
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ikp.ingestion.version_tracker")

class VersionTracker:
    """
    Phase 5: Tracks extraction fingerprints to generate targeted deltas when a PDF is updated.
    """
    
    def __init__(self, registry: Any):
        self.registry = registry

    def compute_fingerprint(self, extracted_objects: List[Any]) -> str:
        """
        Computes a stable hash (fingerprint) of all extracted objects' attributes.
        """
        hasher = hashlib.sha256()
        
        # Sort objects by ID to ensure deterministic hashing
        sorted_objs = sorted(extracted_objects, key=lambda x: getattr(x, "id", str(x)))
        
        for obj in sorted_objs:
            obj_dict = obj.model_dump(mode="json")
            # Remove volatile fields like timestamp, evidence acquisition dates before hashing
            obj_dict.pop("timestamp", None)
            if "evidence" in obj_dict:
                for ev in obj_dict["evidence"]:
                    ev.pop("acquisition_date", None)
                    
            # Convert to stable string representation
            stable_str = str(sorted(obj_dict.items()))
            hasher.update(stable_str.encode('utf-8'))
            
        return hasher.hexdigest()

    def compare_and_generate_deltas(self, source_id: str, old_fingerprint: str, new_fingerprint: str, new_objects: List[Any]) -> Optional[List[Any]]:
        """
        If the fingerprint changed, we generate targeted DeltaChanges.
        If it's the same, we return None (no changes).
        """
        if old_fingerprint == new_fingerprint:
            logger.info(f"Source {source_id} fingerprint unchanged ({new_fingerprint}). No deltas needed.")
            return None
            
        logger.warning(f"Source {source_id} fingerprint changed! Generating targeted deltas.")
        
        from ikp_platform.core.ontology.models import DeltaChange, ChangeType
        
        changes = []
        # In a full implementation we would diff the old objects vs new objects.
        # For now, we simply create a bulk MODIFY delta indicating a new version was published.
        changes.append(DeltaChange(
            object_id="source_version_bump",
            change_type=ChangeType.MODIFY,
            field_name="fingerprint",
            old_value=old_fingerprint,
            new_value=new_fingerprint,
            reason=f"Fingerprint changed for {source_id}. PDF was updated."
        ))
        
        return changes
