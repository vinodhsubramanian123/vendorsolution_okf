import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.ontology.models import Source, EngineeringObjectType, Workload
from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor

logging.basicConfig(level=logging.ERROR)

def main():
    pdf_path = "/media/vinodh/data1/Downloads/HPE Alletra Storage MP B10000 QuickSpecs-a50006985enw.pdf"
    
    source = Source(
        id="source-storage-1",
        source_id="quickspecs-storage-mp",
        source_uri=pdf_path,
        source_type="PDF"
    )
    
    print(f"Running Extractor on: {pdf_path}")
    extractor = PDFExtractor(source)
    objects, delta = extractor.extract(pdf_path)
    
    print(f"\n--- Extracted {len(objects)} Engineering Objects ---")
    
    platforms = [o for o in objects if o.type == EngineeringObjectType.PLATFORM.value]
    if platforms:
        p = platforms[0]
        print(f"✅ Platform Found: {p.id}")
        print(f"  - Title: {p.title}")
        print(f"  - Vendor: {p.vendor}")
        print(f"  - Solution Domain: {p.solution_domain}")
        print(f"  - Product Family: {p.product_family}")
        
        if p.solution_domain == "Storage":
            print("✅ PASS: Correctly identified Solution Domain as 'Storage' (No longer hardcoded as Compute).")
        else:
            print(f"❌ FAIL: Expected Storage, got {p.solution_domain}")
    else:
        print("❌ FAIL: No Platform Extracted!")
        
    components = [o for o in objects if o.type == EngineeringObjectType.COMPONENT.value]
    print(f"\n✅ Components Extracted: {len(components)}")
    for c in components[:3]:
        print(f"  - {c.id}: {c.title} (Domain: {c.solution_domain})")
        
    rules = [o for o in objects if o.type == EngineeringObjectType.RULE.value]
    print(f"\n✅ Engineering Rules Extracted: {len(rules)}")
    if rules:
        r = rules[0]
        print(f"  - Example Rule: {r.id}: {r.expected_outcome[:100]}...")
        if r.solution_domain == "Storage":
             print("✅ PASS: Rule solution domain dynamically inherited as Storage.")
        else:
             print(f"❌ FAIL: Rule domain is {r.solution_domain}")
            
if __name__ == "__main__":
    main()
