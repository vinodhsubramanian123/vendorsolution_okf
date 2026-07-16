import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent.parent))

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.reasoning.rule_engine import RuleEngine

logging.basicConfig(level=logging.ERROR)

def main():
    print("Testing Strict Cross-Domain BOQ Isolation...")
    graph = GraphBuilder()
    
    # Mock Storage Platform
    graph.graph.add_node("hpe-alletra-storage", 
        type="Platform",
        title="HPE Alletra Storage",
        attr_solution_domain="Storage"
    )
    
    # Mock Compute Component (Processor)
    graph.graph.add_node("intel-xeon-gold-6430", 
        type="Component",
        title="Intel Xeon Gold 6430 2.1GHz 32-core",
        attr_solution_domain="Compute"
    )
    
    # Mock Networking Component
    graph.graph.add_node("aruba-cx-8320", 
        type="Component",
        title="Aruba CX 8320 Switch",
        attr_solution_domain="Networking"
    )
    
    engine = RuleEngine(graph)
    
    print("\nScenario 1: Attaching Compute CPU to Storage Array")
    is_valid, chain, errors = engine.evaluate_solution("hpe-alletra-storage", ["intel-xeon-gold-6430"])
    if not is_valid and "CROSS-DOMAIN BLEED DETECTED" in str(errors):
         print("✅ PASS: Engine instantly rejected the Compute component on the Storage platform.")
    else:
         print("❌ FAIL: Engine did not properly isolate the domain.")
         print("Errors:", errors)

    print("\nScenario 2: Attaching Networking Component to Storage Array (Bridge)")
    is_valid, chain, errors = engine.evaluate_solution("hpe-alletra-storage", ["aruba-cx-8320"])
    if "CROSS-DOMAIN BLEED DETECTED" not in str(errors):
         print("✅ PASS: Engine allowed Networking infrastructure as a valid bridge domain.")
    else:
         print("❌ FAIL: Engine wrongly rejected networking.")
         
if __name__ == "__main__":
    main()
