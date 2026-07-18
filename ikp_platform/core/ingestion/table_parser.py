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
        seen_skus = set()
        logger.info(f"Parsing tables and text from {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # PASS 1: Strict Table Extraction
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    if not table or len(table) < 2:
                        continue
                        
                    cleaned_table = []
                    for row in table:
                        cleaned_row = [cell.replace('\n', ' ').strip() if cell else "" for cell in row]
                        cleaned_table.append(cleaned_row)
                        
                    headers = cleaned_table[0]
                    sku_col_indices = []
                    for idx, h in enumerate(headers):
                        h_lower = h.lower()
                        if "sku" in h_lower or "part" in h_lower or "number" in h_lower:
                            sku_col_indices.append(idx)
                            
                    for row in cleaned_table[1:]:
                        for cell_idx, cell_text in enumerate(row):
                            is_sku_col = cell_idx in sku_col_indices
                            sku_match = self.sku_pattern.search(cell_text)
                            
                            if sku_match:
                                sku = sku_match.group(1)
                                if "-" not in sku and not any(c.isdigit() for c in sku):
                                    continue
                                if len(sku_col_indices) > 0 and not is_sku_col:
                                    continue
                                    
                                if sku in seen_skus:
                                    continue
                                
                                brackets = self.bracket_pattern.findall(cell_text)
                                raw_desc = cell_text.replace(sku, "")
                                for b in brackets:
                                    raw_desc = raw_desc.replace(b, "")
                                # Clean up noise prefixes
                                description = raw_desc.strip(" -.,|\n")
                                for p in ["Select the associated trigger SKU", "If the HPE", "•", "−", "-", "*"]:
                                    if description.startswith(p):
                                        description = description[len(p):].strip(" -.,|\n")
                                
                                if len(description) < 30:
                                    prev_desc = row[cell_idx - 1].strip(" -.,|\n") if cell_idx > 0 else ""
                                    next_desc = row[cell_idx + 1].strip(" -.,|\n") if cell_idx + 1 < len(row) else ""
                                    best_desc = prev_desc if len(prev_desc) > len(next_desc) else next_desc
                                    if best_desc:
                                        description = best_desc
                                        
                                role = "dependency_note" if self.sku_pattern.search(description) else "component"
                                    
                                default_qty = 0
                                row_text = " ".join(row)
                                if "default" in row_text.lower() or "qty" in "".join(headers).lower():
                                    qty_match = re.search(r"(\d+)\s+default", row_text, re.IGNORECASE)
                                    if qty_match:
                                        default_qty = int(qty_match.group(1))

                                seen_skus.add(sku)
                                extracted_components.append({
                                    "sku": sku,
                                    "description": description,
                                    "brackets": brackets,
                                    "default_qty": default_qty,
                                    "role": role,
                                    "page": page_num + 1
                                })
                                break

                # PASS 2: Layout Text Fallback (captures SKUs in lists or badly formatted tables)
                text = page.extract_text(layout=True) or ""
                lines = text.split('\n')
                for idx, line in enumerate(lines):
                    # Find all potential SKUs in this line
                    matches = self.sku_pattern.findall(line)
                    for sku in matches:
                        if "-" not in sku and not any(c.isdigit() for c in sku):
                            continue
                        if sku not in seen_skus:
                            seen_skus.add(sku)
                            brackets = self.bracket_pattern.findall(line)
                            
                            # Derive description from the surrounding line text
                            raw_desc = line.replace(sku, "")
                            for b in brackets:
                                raw_desc = raw_desc.replace(b, "")
                            
                            # Clean up noise prefixes
                            description = re.sub(r'\s{2,}', ' ', raw_desc).strip(" -.,|")
                            for p in ["Select the associated trigger SKU", "If the HPE", "•", "−", "-", "*"]:
                                if description.startswith(p):
                                    description = description[len(p):].strip(" -.,|\n")
                            
                            if len(description) < 30:
                                prev_desc = lines[idx-1].strip(" -.,|") if idx > 0 else ""
                                next_desc = lines[idx+1].strip(" -.,|") if idx + 1 < len(lines) else ""
                                prev_desc = re.sub(r'\s{2,}', ' ', prev_desc)
                                next_desc = re.sub(r'\s{2,}', ' ', next_desc)
                                
                                best_desc = prev_desc if len(prev_desc) > len(next_desc) else next_desc
                                if best_desc:
                                    description = best_desc
                                    
                            role = "dependency_note" if self.sku_pattern.search(description) else "component"

                            extracted_components.append({
                                "sku": sku,
                                "description": description,
                                "brackets": brackets,
                                "default_qty": 0,
                                "role": role,
                                "page": page_num + 1
                            })
                            
        logger.info(f"Extracted {len(extracted_components)} structured components from tables and text.")
        return extracted_components
