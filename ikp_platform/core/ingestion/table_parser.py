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
        # Matches standard ProLiant parts (e.g. P03178-B21) and short 6-8 char alphanumeric parts (e.g. S2T40A)
        self.sku_pattern = re.compile(r"\b([A-Z0-9]{6}-[A-Z0-9]{3}|[A-Z0-9]{6,8})\b")
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
                    
                    # Find which column contains SKUs
                    sku_col_indices = []
                    for idx, h in enumerate(headers):
                        h_lower = h.lower()
                        if "sku" in h_lower or "part" in h_lower or "number" in h_lower:
                            sku_col_indices.append(idx)
                            
                    for row in cleaned_table[1:]:
                        for cell_idx, cell_text in enumerate(row):
                            # Only extract SKU if we are in a known SKU column, or if we couldn't find the column 
                            # we fall back to checking all cells but being very strict.
                            is_sku_col = cell_idx in sku_col_indices
                            
                            sku_match = self.sku_pattern.search(cell_text)
                            
                            if sku_match:
                                sku = sku_match.group(1)
                                
                                # Filter out false positives for the short pattern:
                                if "-" not in sku and not any(c.isdigit() for c in sku):
                                    continue
                                    
                                # If we know the SKU columns, and this cell isn't one, it's a false positive (e.g. 6000MT/s in description)
                                if len(sku_col_indices) > 0 and not is_sku_col:
                                    continue
                                    
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
