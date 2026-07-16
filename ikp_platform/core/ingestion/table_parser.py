import re
import pdfplumber
import logging
from typing import List, Dict, Any

logger = logging.getLogger("ikp.ingestion.table_parser")

class TableParser:
    """
    Parses PDF tables using pdfplumber to accurately extract SKUs, 
    bracketed notes (e.g. [OB], (BTO)), and default quantities.
    """
    def __init__(self):
        self.sku_pattern = re.compile(r"\b([A-Z0-9]{6}-[A-Z0-9]{3})\b")
        self.bracket_pattern = re.compile(r"(\[.*?\]|\(.*?\))")

    def parse_document(self, pdf_path: str) -> List[Dict[str, Any]]:
        extracted_components = []
        logger.info(f"Parsing tables from {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    if not table or len(table) < 2:
                        continue
                        
                    # Basic cleaning
                    cleaned_table = []
                    for row in table:
                        cleaned_row = [cell.replace('\n', ' ').strip() if cell else "" for cell in row]
                        cleaned_table.append(cleaned_row)
                        
                    headers = cleaned_table[0]
                    
                    for row in cleaned_table[1:]:
                        for cell_idx, cell_text in enumerate(row):
                            sku_match = self.sku_pattern.search(cell_text)
                            
                            if sku_match:
                                sku = sku_match.group(1)
                                brackets = self.bracket_pattern.findall(cell_text)
                                
                                # Better heuristic for description: 
                                # Remove the SKU and brackets from the cell text.
                                # If empty, maybe the previous cell was the description.
                                raw_desc = cell_text.replace(sku, "")
                                for b in brackets:
                                    raw_desc = raw_desc.replace(b, "")
                                description = raw_desc.strip()
                                
                                if len(description) < 5 and cell_idx > 0:
                                    # Fallback to previous cell if this cell is literally just the SKU
                                    description = row[cell_idx - 1]
                                    
                                # Look for default quantity in headers or row text
                                default_qty = 0
                                row_text = " ".join(row)
                                if "default" in row_text.lower() or "qty" in "".join(headers).lower():
                                    qty_match = re.search(r"(\d+)\s+default", row_text, re.IGNORECASE)
                                    if qty_match:
                                        default_qty = int(qty_match.group(1))

                                component_data = {
                                    "sku": sku,
                                    "description": description.strip(" -,"),
                                    "brackets": brackets,
                                    "default_qty": default_qty,
                                    "page": page_num + 1
                                }
                                extracted_components.append(component_data)
                                break  # Prevent duplicate extraction if SKU appears multiple times in row
                            
        logger.info(f"Extracted {len(extracted_components)} structured components from tables.")
        return extracted_components
