# SKU Extraction & Categorization Learnings

When extracting components and SKUs from vendor PDFs (QuickSpecs, Technical Guides), agents MUST observe the following rules:

## 1. Separate Engineering Components from Commercial SKUs
Following Blueprint 03 §4, engineering knowledge MUST NOT be tied exclusively to a commercial SKU.
- Create an engineering `Component` object representing the physical part and its capabilities.
- Create a separate commercial `SKU` object representing the orderable part number.
- Link them using a `HAS_SKU` engineering relationship.

## 2. Preventing SKU Regex False Positives (The "6000MT" bug)
When extracting SKUs from PDF tables using a Regex, a loose alphanumeric regex (e.g. `[A-Z0-9]{6,8}`) will capture false positives from description columns (e.g., `6000MT/s`, `dl380t`).
- **Rule**: NEVER apply SKU regex blindly across all table cells.
- **Solution**: Parse the table headers first. Identify columns labeled "SKU", "Part", or "Number". ONLY extract SKUs from cells in these designated columns. 

## 3. Avoid "Catch-all" Categorization
Avoid lazy categorizations like dumping unrecognized items into an "Accessory" bucket. 
- Use a comprehensive keyword scoring taxonomy (`COMPONENT_CATEGORY_MAP`) to properly classify parts like TPM modules (Security), Bezels/Rails (Chassis), and Enablement Kits (Infrastructure).

## 4. Post-processing Derived Limits
Not all limits are explicitly written as text (e.g., "Maximum 2 Risers"). Some limits are implicitly derived from the bill of materials.
- Run a post-processing step over the extracted components to synthesize `CategoryLimit` objects (e.g., counting the number of OCP slots extracted to define a max OCP limit).
