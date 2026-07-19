import sys
from pathlib import Path
import logging
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from ikp_platform.core.repository.graph_builder import GraphBuilder  # noqa: E402
from ikp_platform.core.reasoning.rule_engine import RuleEngine  # noqa: E402
from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor  # noqa: E402
from ikp_platform.core.ontology.models import Source, SourceType  # noqa: E402

logging.basicConfig(level=logging.ERROR)


def main():
    print("Testing End-to-End Validation with Real BOQ...")
    graph = GraphBuilder()

    # Ingest the real DL580 Gen12 Platform from PDF
    pdf_path = str(PROJECT_ROOT / "sources" / "pdfs" / "DL580_Gen12_QuickSpecs.pdf")

    source = Source(
        source_id="doc_dl580_gen12",
        source_type=SourceType.PDF,
        original_file_path=pdf_path,
        version="1.0",
    )

    extractor = PDFExtractor(source=source)
    objects, delta = extractor.extract(pdf_path)

    # Load extracted objects into GraphBuilder
    platform_id = None
    for obj in objects:
        if obj.__class__.__name__ == "Platform":
            platform_id = obj.id

        # We manually add it to the internal NetworkX graph for testing
        data = obj.dict()
        node_type = data.pop("type", obj.__class__.__name__)
        graph.graph.add_node(obj.id, type=node_type, **data)

    print(f"Ingested {len(objects)} CTO components from PDF.")
    # Read the Real Excel BOQ
    boq_path = "/media/vinodh/data1/Downloads/HPE_Configs_Proposals/30x HPE_DL580_Gen12_Configuration.xlsx"
    df = pd.read_excel(boq_path)

    component_ids = []
    print(f"\n--- Parsing BOQ: {Path(boq_path).name} ---")
    for idx, row in df.iterrows():
        sku = str(row["SKU"]).strip()
        desc = str(row["Description"]).strip()
        qty = row["Quantity"]

        # Determine Domain heuristically for testing
        domain = "Compute"
        if "switch" in desc.lower() or "cable" in desc.lower():
            domain = "Networking"
        elif (
            "storage" in desc.lower() or "hdd" in desc.lower() or "ssd" in desc.lower()
        ):
            domain = "Storage"

        print(f"Extracted SKU: {sku} - {desc[:30]}... (Qty: {qty}, Domain: {domain})")

        node_id = sku.lower()
        component_ids.append(node_id)

        # Inject into Knowledge Graph
        graph.graph.add_node(
            node_id,
            type="Component",
            title=desc,
            attr_solution_domain=domain,
            evidence=[
                {
                    "confidence": "MEDIUM",
                    "original_text_snippet": f"Parsed from BOQ: {desc}",
                }
            ],
        )

        # Make them compatible for the test
        graph.graph.add_edge(node_id, platform_id, type="CompatibleWith")

    # Now, add a cross-domain bleeder maliciously to test isolation
    graph.graph.add_node(
        "evil-san-array",
        type="Component",
        title="Malicious SAN Array Component",
        attr_solution_domain="Storage",
    )
    component_ids.append("evil-san-array")

    engine = RuleEngine(graph)

    print("\n--- Executing Rule Engine Validation on BOQ ---")
    is_valid, chain, errors = engine.evaluate_solution(platform_id, component_ids)

    print(f"\nValidation Result: {'VALID' if is_valid else 'INVALID (Rejected)'}")
    print("\nReasoning Chain & Traceability:")
    for step in chain:
        print(f"  -> {step}")

    print("\nErrors (Domain Bleeds Blocked):")
    for error in errors:
        print(f"  ❌ {error}")

    if not is_valid and any("CROSS-DOMAIN BLEED DETECTED" in str(e) for e in errors):
        print(
            "\n✅ PASS: The validation engine successfully processed a real Excel BOQ, generated full traceability, and blocked the cross-domain injection!"
        )


if __name__ == "__main__":
    main()
