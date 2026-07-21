import re
import fitz
import hashlib
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import pdfplumber

from ikp_platform.core.ontology.models import (
    Platform,
    BaseEngineeringObject,
    DeltaChange,
    DeltaChangeType,
    Source,
)
from ikp_platform.core.ingestion.adapters.hpe_quickspecs_adapter import HPEQuickSpecsAdapter

logger = logging.getLogger(__name__)

class TableParser:
    def __init__(self):
        pass

    def parse_document(self, file_path: str) -> List[Dict[str, Any]]:
        # Extract components with SKUs and Descriptions
        structured = []
        sku_pattern = re.compile(r"^[A-Z0-9]{6}-[A-Z0-9]{3}$|^[A-Z0-9]{6,8}$", re.IGNORECASE)
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                            
                        clean_row = [str(c).strip() if c else "" for c in row]
                        
                        sku = None
                        description = None
                        
                        # Find the SKU (usually a short alphanumeric code)
                        for cell in clean_row:
                            for word in cell.split():
                                if sku_pattern.match(word):
                                    sku = word.upper()
                                    break
                            if sku:
                                break
                                
                        if not sku:
                            # Also check if it's a raw row with a SKU in it, occasionally joined
                            continue
                            
                        # Find the description (usually the longest cell that is not the SKU)
                        desc_candidates = [c.replace("\n", " ") for c in clean_row if c and c.upper() != sku]
                        if desc_candidates:
                            description = max(desc_candidates, key=len)
                            
                        if not description:
                            continue
                            
                        # Extract bracketed text as tags/capabilities
                        brackets = re.findall(r"\[(.*?)\]|\((.*?)\)", description)
                        brackets_flat = [b[0] or b[1] for b in brackets if (b[0] or b[1])]
                        
                        structured.append({
                            "sku": sku,
                            "description": description,
                            "brackets": brackets_flat,
                            "default_qty": 1,
                            "raw_row": clean_row
                        })
        return structured


class PDFExtractor:
    """
    Extracts canonical ontology objects (Platform, SKU, Rule, etc.) from PDFs.
    Uses an adapter pattern to handle vendor-specific document structures.
    """

    def __init__(self, source: Source, project_root: str = "."):
        self.source = source
        self.project_root = Path(project_root)
        self.extracted_objects: List[BaseEngineeringObject] = []
        self.delta_changes: List[DeltaChange] = []

        # Initialize adapters
        self.adapters = [
            HPEQuickSpecsAdapter(source=source, project_root=project_root)
        ]

    def _normalize_text(self, text: str) -> str:
        """Normalize typography and whitespace."""
        replacements = {
            "\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"', "\u00a0": " "
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        text = re.sub(r"\s+", " ", text)
        return text

    def _human_in_the_loop_fallback(self, text: str) -> Platform:
        """
        Fallback when automated extraction fails or no adapter is found.
        Dumps first 1000 lines to needs_review/<source_id>.json
        """
        logger.warning(
            "Automated Platform Extraction Failed or Confidence < 80%. Triggering HITL fallback."
        )
        # Use project_root for needs_review
        review_dir = self.project_root / "needs_review"
        review_dir.mkdir(exist_ok=True)

        dump_path = review_dir / f"{self.source.source_id}_fallback.txt"
        with open(dump_path, "w", encoding="utf-8") as f:
            f.write(text[:10000])

        logger.info(f"Dumped fallback text to {dump_path} for manual review.")

        return Platform(
            id=f"{self.source.source_id}-manual",
            title="Needs Manual Review",
            vendor="Unknown",
            solution_domain="Unknown",
        )

    def extract(self, file_path: str) -> Tuple[List[BaseEngineeringObject], List[DeltaChange]]:
        logger.info(f"Extracting from PDF: {file_path}")
        doc = fitz.open(file_path)

        if not self.source.version:
            mod_date = doc.metadata.get("modDate")
            if mod_date:
                clean_date = mod_date.strip("D:").replace("'", "")
                self.source.version = f"modDate_{clean_date}"
            else:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()[:12]
                self.source.version = f"sha256_{file_hash}"
            logger.info(f"Computed Deterministic Version: {self.source.version}")

        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n\n"
        doc.close()

        full_text = self._normalize_text(full_text)

        # 1. Find matching adapter
        active_adapter = None
        for adapter in self.adapters:
            if adapter.can_handle(full_text):
                active_adapter = adapter
                logger.info(f"Selected adapter: {adapter.__class__.__name__}")
                break

        if not active_adapter:
            logger.warning("No suitable adapter found for this PDF.")
            platform = self._human_in_the_loop_fallback(full_text)
            self.extracted_objects.append(platform)
            return self.extracted_objects, self.delta_changes

        # 2. Extract Platform
        platform_obj: Optional[Platform] = active_adapter.extract_platform(full_text)
        if not platform_obj:
            platform_obj = self._human_in_the_loop_fallback(full_text)

        self.extracted_objects.append(platform_obj)
        self.delta_changes.append(
            DeltaChange(
                change_type=DeltaChangeType.NEW_OBJECT,
                object_id=platform_obj.id,
                new_value=platform_obj.title,
            )
        )

        # 3. Extract Components & Rules
        table_parser = TableParser()
        structured_components = table_parser.parse_document(file_path)
        
        adapter_objects, adapter_deltas = active_adapter.extract_components(
            full_text, platform_obj, structured_components
        )
        
        self.extracted_objects.extend(adapter_objects)
        self.delta_changes.extend(adapter_deltas)

        logger.info(f"Extracted {len(self.extracted_objects)} canonical objects.")
        return self.extracted_objects, self.delta_changes
