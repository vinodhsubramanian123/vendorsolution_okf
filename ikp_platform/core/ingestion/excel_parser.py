"""
Excel Source Parser — Extracts engineering objects from structured spreadsheets.

Governs: Blueprint 04 §6 (Knowledge Extraction), Blueprint 07 §4 (Extraction Framework)

Spreadsheets are commonly used for BOQs (Bills of Quantities), pricing lists,
and structured configuration rules. This parser converts rows into Pydantic models.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    Component,
    Platform,
    SKU,
    EngineeringObjectType,
    Source,
)

logger = logging.getLogger("ikp.ingestion.excel")


class ExcelExtractor:
    """Parses Excel spreadsheets into IKP canonical objects."""

    def __init__(self):
        pass

    def extract(self, source: Source, file_path: str) -> List[BaseEngineeringObject]:
        """
        Parse the Excel file and return a list of extracted objects.
        Currently handles 'Components' and 'SKUs' sheets if they exist.
        """
        objects = []
        try:
            excel = pd.ExcelFile(file_path)
        except Exception as e:
            logger.error(f"Failed to open Excel file {file_path}: {e}")
            return objects

        sheet_names = excel.sheet_names

        # Extract Components
        if "Components" in sheet_names:
            df = excel.parse("Components")
            objects.extend(self._parse_components(df, source))

        # Extract SKUs
        if "SKUs" in sheet_names:
            df = excel.parse("SKUs")
            objects.extend(self._parse_skus(df, source))

        logger.info(f"ExcelExtractor extracted {len(objects)} objects from {file_path}")
        return objects

    def _parse_components(self, df: pd.DataFrame, source: Source) -> List[Component]:
        """Parse a dataframe of components."""
        components = []
        for _, row in df.iterrows():
            try:
                # Require an ID and Title
                if pd.isna(row.get("ID")) or pd.isna(row.get("Title")):
                    continue

                comp_id = str(row["ID"]).strip()
                
                kwargs = {
                    "id": comp_id,
                    "title": str(row["Title"]).strip(),
                    "description": str(row.get("Description", "")) if pd.notna(row.get("Description")) else None,
                    "vendor": source.vendor,
                    "component_category": str(row.get("Category", "")) if pd.notna(row.get("Category")) else None,
                }
                
                # Extract arbitrary attributes for columns starting with attr_
                # (We don't implement full attribute parsing here for brevity, 
                # but this is the hook for it).

                comp = Component(**kwargs)
                components.append(comp)

            except Exception as e:
                logger.warning(f"Error parsing row in Components sheet: {e}")

        return components

    def _parse_skus(self, df: pd.DataFrame, source: Source) -> List[SKU]:
        """Parse a dataframe of SKUs."""
        skus = []
        for _, row in df.iterrows():
            try:
                if pd.isna(row.get("Part Number")) or pd.isna(row.get("Title")):
                    continue

                pn = str(row["Part Number"]).strip()
                
                kwargs = {
                    "id": f"sku-{pn.lower()}",
                    "title": str(row["Title"]).strip(),
                    "part_number": pn,
                    "price": float(row["Price"]) if pd.notna(row.get("Price")) else None,
                    "currency": str(row.get("Currency", "USD")) if pd.notna(row.get("Currency")) else None,
                }

                sku = SKU(**kwargs)
                skus.append(sku)

            except Exception as e:
                logger.warning(f"Error parsing row in SKUs sheet: {e}")

        return skus
