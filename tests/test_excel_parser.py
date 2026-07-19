import pandas as pd
import tempfile
from pathlib import Path
from ikp_platform.core.ingestion.excel_parser import ExcelExtractor
from ikp_platform.core.ontology.models import Source, SourceType, ProcessingStatus


class TestExcelIngestion:
    def test_excel_extractor_creates_relationships_and_attributes(self):
        # Create a synthetic Excel file
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            temp_path = f.name

        try:
            # Create a dataframe for Components
            components_df = pd.DataFrame(
                {
                    "ID": ["comp-1", "comp-2"],
                    "Title": ["Test Component 1", "Test Component 2"],
                    "Description": ["Desc 1", "Desc 2"],
                    "Category": ["Networking", "Storage"],
                    "attr_Power": ["500W", "200W"],
                    "attr_Weight": [10.5, 5.0],
                }
            )

            # Create a dataframe for SKUs
            skus_df = pd.DataFrame(
                {
                    "Part Number": ["SKU-100", "SKU-200"],
                    "Title": ["SKU 100 Title", "SKU 200 Title"],
                    "Price": [99.99, 149.99],
                    "Currency": ["USD", "USD"],
                }
            )

            with pd.ExcelWriter(temp_path) as writer:
                components_df.to_excel(writer, sheet_name="Components", index=False)
                skus_df.to_excel(writer, sheet_name="SKUs", index=False)

            source = Source(
                id="test-excel",
                source_id="synthetic.xlsx",
                source_type=SourceType.EXCEL,
                status=ProcessingStatus.PENDING,
                vendor="TestVendor",
            )

            extractor = ExcelExtractor()
            platform_id = "test-platform-123"
            objects, delta = extractor.extract(
                source, temp_path, platform_id=platform_id
            )

            assert len(objects) == 4  # 2 components + 2 SKUs

            components = [o for o in objects if o.type.value == "Component"]
            assert len(components) == 2

            comp1 = [c for c in components if c.id == "comp-1"][0]
            assert comp1.title == "Test Component 1"
            assert comp1.component_category == "Networking"

            # Check attributes
            assert len(comp1.attributes) == 2
            power_attr = [a for a in comp1.attributes if a.name == "Power"][0]
            assert power_attr.value == "500W"

            # Check relationships (platform_id linkage)
            assert len(comp1.relationships) == 1
            rel = comp1.relationships[0]
            assert rel.target_id == "test-platform-123"
            assert rel.relationship_type.value == "Compatible With"

            # Check evidence
            assert len(comp1.evidence) == 1
            assert comp1.evidence[0].source_id == "synthetic.xlsx"

            skus = [o for o in objects if o.type.value == "SKU"]
            assert len(skus) == 2
            sku1 = [s for s in skus if s.part_number == "SKU-100"][0]
            assert sku1.price == 99.99

            # Delta checks
            assert delta.source_id == "synthetic.xlsx"
            assert len(delta.changes) == 4

        finally:
            Path(temp_path).unlink(missing_ok=True)
