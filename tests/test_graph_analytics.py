import pytest
import networkx as nx
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.repository.graph_analytics import GraphAnalyticsEngine

def test_articulation_points():
    """Test that articulation points are correctly identified."""
    gb = GraphBuilder()
    
    # Create a graph with an articulation point
    # A - B - C (B is an articulation point)
    gb.graph.add_node("A", type="Component")
    gb.graph.add_node("B", type="Component")
    gb.graph.add_node("C", type="Component")
    
    gb.graph.add_edge("A", "B")
    gb.graph.add_edge("B", "C")
    
    analytics = GraphAnalyticsEngine(gb)
    ap = analytics.get_articulation_points()
    
    assert "B" in ap
    assert "A" not in ap
    assert "C" not in ap
    
    report = analytics.get_fragility_report()
    assert report["total_articulation_points"] == 1
    assert report["critical_nodes"][0]["node_id"] == "B"

def test_subgraph_isomorphism():
    """Test subgraph isomorphism matching for BOQ validation."""
    gb = GraphBuilder()
    analytics = GraphAnalyticsEngine(gb)
    
    bom_graph = nx.DiGraph()
    bom_graph.add_node("server1", type="Platform", attr_component_category="Server")
    bom_graph.add_node("gpu1", type="Component", attr_component_category="GPU")
    bom_graph.add_node("gpu2", type="Component", attr_component_category="GPU")
    bom_graph.add_edge("server1", "gpu1")
    bom_graph.add_edge("server1", "gpu2")
    
    boq_graph = nx.DiGraph()
    boq_graph.add_node("boq_server", type="Platform", attr_component_category="Server")
    boq_graph.add_node("boq_gpu", type="Component", attr_component_category="GPU")
    boq_graph.add_edge("boq_server", "boq_gpu")
    
    # The BOQ structure (1 server -> 1 GPU) exists within the BOM (1 server -> 2 GPUs)
    is_isomorphic = analytics.check_subgraph_isomorphism(boq_graph, bom_graph)
    assert is_isomorphic is True

    # If BOQ asks for 3 GPUs, it should fail
    boq_fail = nx.DiGraph()
    boq_fail.add_node("boq_server", type="Platform")
    boq_fail.add_node("boq_gpu1", type="Component", attr_component_category="GPU")
    boq_fail.add_node("boq_gpu2", type="Component", attr_component_category="GPU")
    boq_fail.add_node("boq_gpu3", type="Component", attr_component_category="GPU")
    boq_fail.add_edge("boq_server", "boq_gpu1")
    boq_fail.add_edge("boq_server", "boq_gpu2")
    boq_fail.add_edge("boq_server", "boq_gpu3")
    
    is_isomorphic_fail = analytics.check_subgraph_isomorphism(boq_fail, bom_graph)
    assert is_isomorphic_fail is False

def test_compute_vendor_solution_score():
    """Test heuristic solution scoring logic."""
    gb = GraphBuilder()
    analytics = GraphAnalyticsEngine(gb)
    
    boq_nodes = [
        {"attr_component_category": "CPU"},
        {"attr_component_category": "GPU"},
        {"attr_component_category": "Cable"}
    ]
    
    # BOM has CPU, GPU, but missing Cable
    bom_nodes = [
        {"attr_component_category": "CPU"},
        {"attr_component_category": "GPU"}
    ]
    
    result = analytics.compute_vendor_solution_score(boq_nodes, bom_nodes)
    
    # Cable is missing, so component match ratio is 2/3 (0.6667)
    # CPU and GPU are critical. 2/2 critical found, so critical match ratio is 1.0
    # Score = (0.6667 * 0.4) + (1.0 * 0.6) = 0.26668 + 0.6 = 0.8667
    
    assert result["critical_match_ratio"] == 1.0
    assert result["component_match_ratio"] == pytest.approx(0.6667, abs=1e-3)
    assert "Cable" in result["missing_categories"]
    assert "GPU" not in result["missing_categories"]
    assert result["score"] == pytest.approx(0.8667, abs=1e-3)

def test_tough_subgraph_isomorphism():
    """Test a complex tough case for subgraph isomorphism with identical node types."""
    gb = GraphBuilder()
    analytics = GraphAnalyticsEngine(gb)
    
    # BOM Graph: A ring topology with a central hub
    bom_graph = nx.DiGraph()
    for i in range(5):
        bom_graph.add_node(f"node_{i}", type="Component", attr_component_category="Generic")
    bom_graph.add_node("hub", type="Platform", attr_component_category="Hub")
    
    # Connect hub to all
    for i in range(5):
        bom_graph.add_edge("hub", f"node_{i}")
    # Connect ring
    for i in range(5):
        bom_graph.add_edge(f"node_{i}", f"node_{(i+1)%5}")
        
    # BOQ Graph: A requested star topology (hub to 3 nodes) but missing the ring connections
    boq_graph = nx.DiGraph()
    boq_graph.add_node("req_hub", type="Platform", attr_component_category="Hub")
    for i in range(3):
        boq_graph.add_node(f"req_node_{i}", type="Component", attr_component_category="Generic")
        boq_graph.add_edge("req_hub", f"req_node_{i}")
        
    # The star topology (hub + 3 nodes) IS isomorphic to a subgraph of the BOM
    assert analytics.check_subgraph_isomorphism(boq_graph, bom_graph) is True
    
    # Now ask for a ring of 4, which exists in BOM (any 4 nodes in the 5-ring)
    boq_ring = nx.DiGraph()
    for i in range(4):
        boq_ring.add_node(f"req_ring_{i}", type="Component", attr_component_category="Generic")
        boq_ring.add_edge(f"req_ring_{i}", f"req_ring_{(i+1)%4}")
        
    # A 4-ring does NOT exist in a 5-ring (without the 5th node, it's just a line)
    # Therefore, subgraph isomorphism should fail!
    assert analytics.check_subgraph_isomorphism(boq_ring, bom_graph) is False
