import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.ontology.models import Source, EngineeringObjectType, Workload
from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor

logging.basicConfig(level=logging.ERROR)

def main():
    pdf_path = "/media/vinodh/data1/Downloads/PrevGoogleStudioScripts/HPE ProLiant Compute DL380 Gen12 QuickSpecs-a00073551enw.pdf"
    
    source = Source(
        id="source-1",
        source_id="quickspecs-gen12",
        source_uri=pdf_path,
        source_type="PDF"
    )
    
    print(f"Running Extractor on: {pdf_path}")
    extractor = PDFExtractor(source)
    objects, delta = extractor.extract(pdf_path)
    
    print(f"\n--- Extracted {len(objects)} Engineering Objects ---")
    
    platforms = [o for o in objects if o.type == EngineeringObjectType.PLATFORM.value]
    if platforms:
        print(f"✅ Platform Found: {platforms[0].id} (Title: {platforms[0].title})")
        
        # Verify no cross-bleed
        if "gen12" in platforms[0].id.lower() and "hpe" in platforms[0].id.lower():
            print(f"✅ PASS: Platform explicitly sandboxed to vendor/generation: {platforms[0].id}")
        else:
            print(f"❌ FAIL: Platform ID doesn't isolate vendor/generation: {platforms[0].id}")
    else:
        print("❌ FAIL: No Platform Extracted!")
        
    workloads = [o for o in objects if getattr(o, "type", None) == EngineeringObjectType.WORKLOAD.value]
    print(f"\n✅ Workloads Extracted ({len(workloads)}):")
    for w in workloads:
        print(f"  - {w.title} ({w.id})")
        
    if len(workloads) == 0:
        print("❌ FAIL: No Workloads Extracted! Check introductory text scanning.")
        
    rules = [o for o in objects if o.type == EngineeringObjectType.RULE.value]
    print(f"\n✅ Engineering Rules Extracted: {len(rules)}")
    for r in rules[:3]:
        print(f"  - {r.id}: {r.expected_outcome[:100]}...")
        
    # Check rule IDs for Gen12 isolation
    if rules:
        cross_bleed = any("gen11" in r.id.lower() for r in rules)
        if cross_bleed:
            print("❌ FAIL: Cross-bleed detected! Gen11 rules found in Gen12 document.")
        else:
            print("✅ PASS: All rules strictly sandboxed to Gen12.")
            
if __name__ == "__main__":
    main()
