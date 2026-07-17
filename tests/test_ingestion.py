import pytest
from ikp_platform.core.ingestion.pdf_extractor import PDFExtractor
from ikp_platform.core.ontology.models import Source, SourceType, ProcessingStatus, Platform

class TestIngestion:
    def setup_method(self):
        self.source = Source(
            id="test-source",
            source_id="dummy.pdf",
            source_type=SourceType.PDF,
            status=ProcessingStatus.PENDING
        )
        self.extractor = PDFExtractor(self.source)
        self.platform = Platform(
            id="dl380-gen12",
            title="HPE ProLiant DL380 Gen12",
            vendor="HPE",
            solution_domain="Compute",
            product_family="ProLiant",
            generation="Gen12"
        )

    from unittest.mock import patch, MagicMock
    from ikp_platform.core.ontology.models import Rule, RuleSeverity

    @patch("ikp_platform.core.reasoning.llm_client.LLMClient")
    def test_rule_extraction(self, mock_llm_class):
        # Setup mock to return a pre-defined JSON response instead of opening a browser
        mock_instance = mock_llm_class.return_value
        mock_instance.extract_rules.return_value = [{"rule_text": "Requires Qty 1 of 65cm Quick Disconnect Tube Set FIO Kit", "severity": "Error", "trigger_conditions": ["tube selected"]}]
        mock_instance.critic_review_rules.return_value = [{"rule_text": "Requires Qty 1 of 65cm Quick Disconnect Tube Set FIO Kit", "severity": "Error", "trigger_conditions": ["tube selected"]}]
        
        # Override the extractor's llm_client with our mock
        self.extractor.llm_client = mock_instance
        
        text = "- Requires Qty 1 of 65cm Quick Disconnect Tube Set FIO Kit (P62038-B21).\n"
        text += "Important: Cannot be selected with the NS204i-u Rear Enable Kit (P74755-B21)."
        
        rules = self.extractor._extract_rules(text, self.platform)
        
        # The exact length depends on the mock, but we verify it parsed our mock
        assert len(rules) >= 1
        
        # Verify Requires rule
        req_rule = [r for r in rules if "Requires" in r.description]
        assert len(req_rule) > 0
        assert req_rule[0].severity.value == "Error"
        
    def test_structured_components(self):
        structured_data = [
            {
                "sku": "P48803-B21",
                "description": "Primary Riser Option-2",
                "brackets": ["(P48803-B21)"],
                "default_qty": 0,
                "page": 15
            }
        ]
        
        components = self.extractor._process_structured_components(structured_data, self.platform)
        assert len(components) == 2
        comp = [c for c in components if c.type.value == "Component"][0]
        sku = [c for c in components if c.type.value == "SKU"][0]
        assert comp.title.startswith("P48803-B21")
        assert sku.title == "SKU P48803-B21"
