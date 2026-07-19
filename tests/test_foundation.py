"""
Regression tests for IKP V1.0 Phase 1 — Foundation Layer.

Tests:
1. Ontology model creation and serialization
2. OKF Writer produces valid OKF Markdown with correct frontmatter
3. OKF Reader round-trips correctly (write → read → compare)
4. Graph Builder metadata filtering and relationship traversal
5. Repository Manager bootstrap and sync
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from ikp_platform.core.ontology.models import (
    BaseEngineeringObject,
    EngineeringObjectType,
    EngineeringRelationship,
    RelationshipType,
    EngineeringAttribute,
    EvidenceRecord,
    ConfidenceLevel,
    LifecycleStatus,
    Platform,
    Component,
    Rule,
    RuleSeverity,
    Constraint,
    Source,
    SourceType,
    ProcessingStatus,
    KnowledgeDelta,
    DeltaChange,
    DeltaChangeType,
    DeltaStatus,
    CustomerRequest,
    CustomerRequirement,
    SolutionCandidate,
    Workload,
)
from ikp_platform.core.repository.okf_writer import OKFWriter
from ikp_platform.core.repository.okf_reader import OKFReader
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.repository.repo_manager import RepoManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test artifacts."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


# -----------------------------------------------------------------------
# 1. Ontology Model Tests
# -----------------------------------------------------------------------

class TestOntologyModels:
    def test_platform_creation(self):
        platform = Platform(
            id="storage/alletra/6000/alletra-6050",
            title="Alletra 6050",
            description="HPE Alletra 6050 Block Storage Platform",
            vendor="HPE",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
            lifecycle_status=LifecycleStatus.ACTIVE,
            capabilities=["NVMe", "Replication", "High Availability"],
            tags=["storage", "block", "nvme"],
        )
        assert platform.type == EngineeringObjectType.PLATFORM
        assert platform.vendor == "HPE"
        assert "NVMe" in platform.capabilities

    def test_rule_creation_with_full_fields(self):
        """Blueprint 03 §8: Rule must expose scope, confidence, evidence, version."""
        rule = Rule(
            id="rules/max-controllers",
            title="Maximum Controllers Rule",
            scope="Platform",
            severity=RuleSeverity.ERROR,
            confidence=ConfidenceLevel.HIGH,
            applicable_objects=["storage/alletra/6000/alletra-6050"],
            trigger_conditions=["controller_count > 4"],
            expected_outcome="Reject configurations exceeding 4 controllers",
            version=2,
            evidence=[EvidenceRecord(
                source_id="SRC-quickspec-001",
                confidence=ConfidenceLevel.HIGH,
                description="HPE QuickSpecs page 42",
            )],
        )
        assert rule.scope == "Platform"
        assert rule.confidence == ConfidenceLevel.HIGH
        assert rule.version == 2
        assert len(rule.evidence) == 1

    def test_source_registration(self):
        """Blueprint 04 §5: Source must have permanent identity with full metadata."""
        source = Source(
            source_type=SourceType.PDF,
            vendor="HPE",
            product_family="Alletra",
            product_generation="6000",
            version="1.0",
            original_file_path="sources/pdfs/alletra_6000_quickspec.pdf",
            processing_status=ProcessingStatus.PENDING,
        )
        assert source.source_id.startswith("SRC-")
        assert source.source_type == SourceType.PDF
        assert source.processing_status == ProcessingStatus.PENDING

    def test_knowledge_delta_creation(self):
        """Blueprint 02 §7: Knowledge Delta with changes list."""
        delta = KnowledgeDelta(
            source_id="SRC-001",
            changes=[
                DeltaChange(
                    change_type=DeltaChangeType.NEW_OBJECT,
                    object_id="storage/alletra/6000/alletra-6050",
                    new_value="New platform added",
                ),
                DeltaChange(
                    change_type=DeltaChangeType.NEW_RULE,
                    object_id="rules/max-controllers",
                    field_name="limit_value",
                    new_value=4,
                ),
            ],
        )
        assert delta.delta_id.startswith("DELTA-")
        assert delta.status == DeltaStatus.PENDING
        assert len(delta.changes) == 2

    def test_solution_candidate(self):
        """Blueprint 05 §13: Solution must include reasoning and confidence."""
        solution = SolutionCandidate(
            request_id="REQ-001",
            profile="Balanced",
            components=["alletra-6050", "controller-a", "drive-nvme-1"],
            reasoning_chain=[
                "Customer requires AI-ready storage",
                "Filtered by workload=AI, domain=Storage",
                "Alletra 6050 supports NVMe and AI workloads",
            ],
            requirements_satisfied=["High Performance", "NVMe", "AI Ready"],
            confidence=ConfidenceLevel.HIGH,
        )
        assert solution.profile == "Balanced"
        assert len(solution.reasoning_chain) == 3


# -----------------------------------------------------------------------
# 2. OKF Writer Tests
# -----------------------------------------------------------------------

class TestOKFWriter:
    def test_writes_valid_frontmatter(self, temp_dir):
        writer = OKFWriter(temp_dir)
        obj = Platform(
            id="alletra-6050",
            title="Alletra 6050",
            description="HPE Alletra 6050 Block Storage",
            vendor="HPE",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
            capabilities=["NVMe", "Replication"],
            tags=["storage", "block"],
        )
        path = writer.write_concept(obj)

        # Verify file exists
        full_path = Path(temp_dir) / path
        assert full_path.exists()

        # Verify frontmatter
        content = full_path.read_text()
        assert content.startswith("---")
        assert "type: Platform" in content
        assert "vendor: HPE" in content
        assert "solution_domain: Storage" in content

    def test_hierarchical_path(self, temp_dir):
        writer = OKFWriter(temp_dir)
        obj = Platform(
            id="alletra-6050",
            title="Alletra 6050",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
        )
        path = writer.write_concept(obj)
        assert "storage" in path
        assert "alletra" in path
        assert "6000" in path

    def test_hierarchical_path_component(self, temp_dir):
        writer = OKFWriter(temp_dir)
        obj = Component(
            id="xeon-6527p",
            title="Xeon 6527P",
            vendor="Intel",
            solution_domain="Compute",
            product_family="ProLiant",
            generation="Gen12",
            platform_id="hpe-proliant-dl380-gen12",
            component_category="CPU",
        )
        path = writer.write_concept(obj)
        assert "compute" in path
        assert "proliant" in path
        assert "gen12" in path
        assert "hpe-proliant-dl380-gen12" in path
        assert "components" in path
        assert "cpu" in path

    def test_generates_index(self, temp_dir):
        writer = OKFWriter(temp_dir)
        obj = Platform(
            id="alletra-6050",
            title="Alletra 6050",
            description="Test platform",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
        )
        writer.write_concept(obj)

        # Generate index for the directory containing the file
        file_path = writer._compute_path(obj)
        writer.generate_index(file_path.parent)

        index_path = file_path.parent / "index.md"
        assert index_path.exists()

    def test_log_entry(self, temp_dir):
        writer = OKFWriter(temp_dir)
        writer.append_log_entry("Creation", "Test entry", "test.md")

        log_path = Path(temp_dir) / "log.md"
        assert log_path.exists()
        content = log_path.read_text()
        assert "**Creation**" in content


# -----------------------------------------------------------------------
# 3. OKF Reader Tests (Round-trip)
# -----------------------------------------------------------------------

class TestOKFReader:
    def test_round_trip(self, temp_dir):
        """Write an object, read it back, verify key fields match."""
        writer = OKFWriter(temp_dir)
        original = Platform(
            id="alletra-6050",
            title="Alletra 6050",
            description="HPE Alletra 6050 Block Storage",
            vendor="HPE",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
            capabilities=["NVMe", "Replication"],
            tags=["storage", "block"],
            lifecycle_status=LifecycleStatus.ACTIVE,
        )
        writer.write_concept(original)

        reader = OKFReader(temp_dir)
        objects = reader.load_all()

        assert len(objects) >= 1
        loaded = objects[0]
        assert loaded.title == "Alletra 6050"
        assert loaded.vendor == "HPE"
        assert loaded.solution_domain == "Storage"
        assert "NVMe" in loaded.capabilities


# -----------------------------------------------------------------------
# 4. Graph Builder Tests
# -----------------------------------------------------------------------

class TestGraphBuilder:
    def _build_test_graph(self):
        """Create a small test graph with known structure."""
        graph = GraphBuilder()

        platform = BaseEngineeringObject(
            id="alletra-6050",
            type=EngineeringObjectType.PLATFORM,
            title="Alletra 6050",
            vendor="HPE",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
            capabilities=["NVMe", "Replication", "AI"],
            relationships=[
                EngineeringRelationship(
                    target_id="controller-a",
                    relationship_type=RelationshipType.CONTAINS,
                ),
                EngineeringRelationship(
                    target_id="firmware-1.30",
                    relationship_type=RelationshipType.REQUIRES,
                ),
            ],
        )
        graph.add_concept(platform)

        controller = BaseEngineeringObject(
            id="controller-a",
            type=EngineeringObjectType.COMPONENT,
            title="Controller A",
            vendor="HPE",
            solution_domain="Storage",
            capabilities=["NVMe"],
        )
        graph.add_concept(controller)

        compute = BaseEngineeringObject(
            id="dl380-gen11",
            type=EngineeringObjectType.PLATFORM,
            title="DL380 Gen11",
            vendor="HPE",
            solution_domain="Compute",
            capabilities=["GPU", "AI"],
        )
        graph.add_concept(compute)

        return graph

    def test_filter_by_vendor(self):
        graph = self._build_test_graph()
        results = graph.filter_by_metadata({"vendor": "HPE"})
        assert len(results) == 3

    def test_filter_by_solution_domain(self):
        graph = self._build_test_graph()
        results = graph.filter_by_metadata({"solution_domain": "Storage"})
        assert len(results) == 2  # alletra-6050 and controller-a

    def test_filter_by_capabilities(self):
        graph = self._build_test_graph()
        results = graph.filter_by_capabilities(["NVMe", "AI"])
        assert "alletra-6050" in results

    def test_traverse_relationships(self):
        graph = self._build_test_graph()
        rels = graph.traverse_relationships("alletra-6050", "Contains")
        assert len(rels) == 1
        assert rels[0]["target"] == "controller-a"

    def test_get_dependencies(self):
        graph = self._build_test_graph()
        deps = graph.get_dependencies("alletra-6050")
        assert "firmware-1.30" in deps

    def test_stats(self):
        graph = self._build_test_graph()
        stats = graph.get_stats()
        # 3 explicit nodes + 1 auto-created by NetworkX (firmware-1.30 edge target)
        assert stats["total_nodes"] == 4
        assert stats["total_edges"] == 2

    def test_filter_by_component_category(self):
        graph = self._build_test_graph()
        
        gpu = Component(
            id="gpu-h100",
            title="NVIDIA H100",
            vendor="NVIDIA",
            component_category="GPU"
        )
        graph.add_concept(gpu)
        
        results = graph.filter_by_metadata({"component_category": "GPU"})
        assert "gpu-h100" in results
        assert len(results) == 1

    def test_filter_by_workload_type(self):
        graph = self._build_test_graph()
        
        workload = Workload(
            id="wl-ai-training",
            title="AI Training",
            performance_requirements={"tflops": 1000}
        )
        graph.add_concept(workload)
        
        results = graph.filter_by_metadata({"type": EngineeringObjectType.WORKLOAD.value})
        assert "wl-ai-training" in results
        
        type_results = graph.filter_by_type(EngineeringObjectType.WORKLOAD.value)
        assert "wl-ai-training" in type_results

    def test_filter_by_custom_attributes(self):
        graph = self._build_test_graph()
        
        platform = Platform(
            id="server-1",
            title="Server with Attributes",
            attributes=[
                EngineeringAttribute(name="Rack Units", value=2),
                EngineeringAttribute(name="Form Factor", value="Rack")
            ]
        )
        graph.add_concept(platform)
        
        results = graph.filter_by_metadata({"attr_rack_units": 2})
        assert "server-1" in results
        
        results2 = graph.filter_by_metadata({"attr_form_factor": "Rack"})
        assert "server-1" in results2

    def test_filter_by_workload_requirements(self):
        graph = self._build_test_graph()
        
        workload = Workload(
            id="wl-ai",
            title="AI Workload",
            performance_requirements={"tflops": 1000},
            capacity_requirements={"storage_tb": 50}
        )
        graph.add_concept(workload)
        
        results_perf = graph.filter_by_metadata({"req_perf_tflops": 1000})
        assert "wl-ai" in results_perf
        
        results_cap = graph.filter_by_metadata({"req_cap_storage_tb": 50})
        assert "wl-ai" in results_cap

    def test_filter_by_rule_and_constraint(self):
        graph = self._build_test_graph()
        
        rule = Rule(
            id="rule-1",
            title="Max Drives Rule",
            scope="Storage",
            severity=RuleSeverity.CRITICAL
        )
        graph.add_concept(rule)
        
        constraint = Constraint(
            id="const-1",
            title="Max Drives Constraint",
            limit_name="max_drives",
            limit_value=24
        )
        graph.add_concept(constraint)
        
        res_rule = graph.filter_by_metadata({"scope": "Storage", "severity": RuleSeverity.CRITICAL.value})
        assert "rule-1" in res_rule
        
        res_const = graph.filter_by_metadata({"limit_name": "max_drives", "limit_value": 24})
        assert "const-1" in res_const

    def test_build_subgraph(self):
        graph = self._build_test_graph()
        
        # Test creating a subgraph with a subset of nodes
        subgraph = graph.build_subgraph(["alletra-6050", "controller-a"])
        
        # Verify the subgraph only contains the requested nodes
        assert subgraph.number_of_nodes() == 2
        assert "alletra-6050" in subgraph.nodes
        assert "controller-a" in subgraph.nodes
        
        # Verify edges are preserved in the induced subgraph
        assert subgraph.has_edge("alletra-6050", "controller-a")
        
        # Verify excluded nodes and their edges are missing
        assert "dl380-gen11" not in subgraph.nodes
        assert not subgraph.has_edge("alletra-6050", "firmware-1.30")



# -----------------------------------------------------------------------
# 5. Repository Manager Tests
# -----------------------------------------------------------------------

class TestRepoManager:
    def test_add_and_bootstrap(self, temp_dir):
        repo_path = str(Path(temp_dir) / "repository")
        manager = RepoManager(repo_path, temp_dir)

        obj = Platform(
            id="alletra-6050",
            title="Alletra 6050",
            vendor="HPE",
            solution_domain="Storage",
            product_family="Alletra",
            generation="6000",
        )
        manager.add_concept(obj)

        # Verify STATE.md was created
        state_path = Path(temp_dir) / "STATE.md"
        assert state_path.exists()

        # Verify LOG.md was created
        log_path = Path(temp_dir) / "LOG.md"
        assert log_path.exists()

        # Test bootstrap — create a fresh manager and load
        manager2 = RepoManager(repo_path, temp_dir)
        count = manager2.bootstrap()
        assert count >= 1
        assert manager2.graph.graph.number_of_nodes() >= 1
