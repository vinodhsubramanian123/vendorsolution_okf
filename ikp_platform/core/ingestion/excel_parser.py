"""
Excel Source Parser — Extracts engineering objects from structured spreadsheets.

Governs: Blueprint 04 §6 (Knowledge Extraction), Blueprint 07 §4 (Extraction Framework)

Spreadsheets are commonly used for BOQs (Bills of Quantities), pricing lists,
and structured configuration rules. This parser converts rows into Pydantic models.
"""

import pandas as pd
from typing import List, Optional, Tuple
import logging

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    Component,
    SKU,
    EngineeringObjectType,
    EngineeringAttribute,
    EngineeringRelationship,
    RelationshipType,
    Source,
    KnowledgeDelta,
    DeltaChange,
    DeltaChangeType,
    EvidenceRecord,
    ConfidenceLevel,
)

logger = logging.getLogger("ikp.ingestion.excel")


class ExcelExtractor:
    """Parses Excel spreadsheets into IKP canonical objects."""

    def extract(
        self,
        source: Source,
        file_path: str,
        platform_id: Optional[str] = None,
    ) -> Tuple[List[BaseEngineeringObject], KnowledgeDelta]:
        """
        Parse the Excel file and return a tuple of (extracted objects, KnowledgeDelta).
        Currently handles 'Components' and 'SKUs' sheets if they exist.

        `platform_id`: if given, every parsed Component gets a
        COMPATIBLE_WITH relationship to this platform ID, so it's
        actually reachable by solution generation (which walks
        relationships from a platform node, not a bare node list).
        Without it, parsed components are added to the repository but
        will never be selected for any solution -- that's made loud
        here rather than a silent gap, since it isn't obvious from the
        API surface alone.
        """
        objects = []
        try:
            excel = pd.ExcelFile(file_path)
        except Exception as e:
            logger.error(f"Failed to open Excel file {file_path}: {e}")
            return objects, KnowledgeDelta(source_id=source.source_id)

        sheet_names = excel.sheet_names

        # Extract Components
        if "Components" in sheet_names:
            df = excel.parse("Components")
            objects.extend(self._parse_components(df, source, platform_id))

        # Extract SKUs
        if "SKUs" in sheet_names:
            df = excel.parse("SKUs")
            objects.extend(self._parse_skus(df, source))

        if "Components" in sheet_names and not platform_id:
            logger.warning(
                "ExcelExtractor: no platform_id given -- %d component(s) from "
                "%s were added to the repository with no COMPATIBLE_WITH "
                "relationship. They will be ingested but never selected by "
                "solution generation until linked to a platform.",
                len(objects),
                file_path,
            )

        # Create delta records for the extracted objects
        changes = []
        for obj in objects:
            ctype = (
                DeltaChangeType.NEW_COMPONENT
                if obj.type == EngineeringObjectType.COMPONENT
                else DeltaChangeType.NEW_SKU
            )
            changes.append(
                DeltaChange(
                    change_type=ctype,
                    object_id=obj.id,
                    evidence=EvidenceRecord(
                        source_id=source.source_id,
                        confidence=ConfidenceLevel.HIGH,
                        description=f"Extracted {obj.type.value} from Excel {source.source_id}",
                    ),
                )
            )

        delta = KnowledgeDelta(source_id=source.source_id, changes=changes)

        logger.info(f"ExcelExtractor extracted {len(objects)} objects from {file_path}")
        return objects, delta

    def _parse_components(
        self, df: pd.DataFrame, source: Source, platform_id: Optional[str] = None
    ) -> List[Component]:
        """Parse a dataframe of components."""
        components = []
        evidence = [
            EvidenceRecord(
                source_id=source.source_id,
                confidence=ConfidenceLevel.HIGH,
                description=f"Extracted from Excel row in {source.source_id}",
            )
        ]
        attr_columns = [c for c in df.columns if str(c).lower().startswith("attr_")]

        for _, row in df.iterrows():
            try:
                # Require an ID and Title
                if pd.isna(row.get("ID")) or pd.isna(row.get("Title")):
                    continue

                comp_id = str(row["ID"]).strip()

                attributes = []
                for col in attr_columns:
                    val = row.get(col)
                    if pd.notna(val):
                        attributes.append(
                            EngineeringAttribute(
                                name=str(col)[len("attr_") :],
                                value=val.item() if hasattr(val, "item") else val,
                            )
                        )

                relationships = []
                if platform_id:
                    relationships.append(
                        EngineeringRelationship(
                            target_id=platform_id,
                            relationship_type=RelationshipType.COMPATIBLE_WITH,
                            evidence=evidence,
                        )
                    )

                kwargs = {
                    "id": comp_id,
                    "title": str(row["Title"]).strip(),
                    "description": str(row.get("Description", ""))
                    if pd.notna(row.get("Description"))
                    else None,
                    "vendor": source.vendor,
                    "component_category": str(row.get("Category", ""))
                    if pd.notna(row.get("Category"))
                    else None,
                    "evidence": evidence,
                    "attributes": attributes,
                    "relationships": relationships,
                }

                comp = Component(**kwargs)
                components.append(comp)

            except Exception as e:
                logger.warning(f"Error parsing row in Components sheet: {e}")

        return components

    def _parse_skus(self, df: pd.DataFrame, source: Source) -> List[SKU]:
        """Parse a dataframe of SKUs."""
        skus = []
        evidence = [
            EvidenceRecord(
                source_id=source.source_id,
                confidence=ConfidenceLevel.HIGH,
                description=f"Extracted from Excel row in {source.source_id}",
            )
        ]
        for _, row in df.iterrows():
            try:
                if pd.isna(row.get("Part Number")) or pd.isna(row.get("Title")):
                    continue

                pn = str(row["Part Number"]).strip()

                kwargs = {
                    "id": f"sku-{pn.lower()}",
                    "title": str(row["Title"]).strip(),
                    "part_number": pn,
                    "price": float(row["Price"])
                    if pd.notna(row.get("Price"))
                    else None,
                    "currency": str(row.get("Currency", "USD"))
                    if pd.notna(row.get("Currency"))
                    else None,
                    "evidence": evidence,
                }

                sku = SKU(**kwargs)
                skus.append(sku)

            except Exception as e:
                logger.warning(f"Error parsing row in SKUs sheet: {e}")

        return skus
