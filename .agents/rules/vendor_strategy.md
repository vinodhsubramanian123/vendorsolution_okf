# Multi-Vendor Ingestion Strategy

As the platform scales to support Dell, Cisco, Lenovo, and other vendors, hardcoding regex patterns or keyword lists into the core `TableParser` or `PDFExtractor` will become unmaintainable. 

Future agents MUST implement the following architectural strategy for multi-vendor support:

## 1. Vendor Strategy Pattern
We will refactor the ingestion engine to use a **Strategy Pattern** based on Vendor Profiles.
- `ikp_platform/core/ingestion/profiles/base_profile.py`
- `ikp_platform/core/ingestion/profiles/hpe_profile.py`
- `ikp_platform/core/ingestion/profiles/dell_profile.py`

## 2. Vendor-Specific SKU Regex
Instead of `self.sku_pattern = re.compile(...)` in the generic `TableParser`, the parser will receive the regex from the active vendor profile.
- HPE uses `[A-Z0-9]{6}-[A-Z0-9]{3}` (e.g. `P03178-B21`) and short alphanumerics.
- Dell uses 5-8 digit alphanumeric Option IDs, Customer Kits (e.g., `384-BDTF`, `400-BNOO`).
- Cisco uses PID formats (e.g., `UCSC-C220-M6S`, `UCS-MR-X32G2RW`).
The profile will define `get_sku_pattern()` to cleanly handle this divergence.

## 3. Taxonomy Mapping Overlays
While the engineering taxonomy (`CPU`, `Memory/DIMM`, `Storage/Controller`) remains universal, different vendors use different marketing terms.
- HPE uses "Smart Array"
- Dell uses "PERC" (PowerEdge RAID Controller)
- Cisco uses "Cisco 12G Modular RAID"
The `COMPONENT_CATEGORY_MAP` will be moved into the Vendor Profiles so that keyword scoring accurately maps vendor-specific marketing terms to the universal engineering taxonomy.

## 4. Format-Specific Table Extraction
Dell Technical Guides often use different table layouts (e.g., merging description and SKU into a single column, or splitting them across multiple rows). The vendor profile will dictate the heuristic used by `TableParser` (e.g., `parse_dell_table_layout()`).
