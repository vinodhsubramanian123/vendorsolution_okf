import sys
import logging
from unittest.mock import MagicMock
from ikp_platform.core.workflow.executor import WorkflowExecutor
from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import *

logging.basicConfig(level=logging.INFO)

graph = GraphBuilder()
wl = Workload(id="wl-ai", title="AI Workload", solution_domain="Compute")
graph.add_concept(wl)

plat = Platform(
    id="hpe-proliant-dl380-gen12",
    title="DL380",
    capabilities=["wl-ai"],
    relationships=[EngineeringRelationship(target_id="wl-ai", relationship_type=RelationshipType.SUPPORTS)]
)
graph.add_concept(plat)

cpu = Component(
    id="hpe-proliant-dl380-gen12-processors-xeon-6505p",
    title="Xeon 6505P",
    component_category="CPU",
    relationships=[EngineeringRelationship(target_id="hpe-proliant-dl380-gen12", relationship_type=RelationshipType.COMPATIBLE_WITH)]
)
graph.add_concept(cpu)

mem = Component(
    id="hpe-proliant-dl380-gen12-components-6000mt",
    title="6000MT Memory",
    component_category="MEMORY",
    relationships=[EngineeringRelationship(target_id="hpe-proliant-dl380-gen12", relationship_type=RelationshipType.COMPATIBLE_WITH)]
)
graph.add_concept(mem)

executor = WorkflowExecutor(graph)

req = CustomerRequest(
    request_id="test-2",
    workloads=["wl-ai"],
    requirements=[]
)
executor.parser.parse_request = MagicMock(return_value=req)

def mock_evaluate(platform_id, components):
    errors = []
    cats = [graph.graph.nodes[c].get("attr_component_category", "").upper() if c in graph.graph else "" for c in components]
    missing = []
    for mandatory in ["CPU", "MEMORY"]:
        if mandatory not in cats:
            missing.append(mandatory)
    if missing:
        errors.append(f"Missing core categories: {','.join(missing)}")
    
    is_valid = len(errors) == 0
    print(f"[EVALUATE] components={components} errors={errors} is_valid={is_valid}")
    return is_valid, ["Mock validation run"], errors

executor.rule_engine.evaluate_solution = MagicMock(side_effect=mock_evaluate)
executor.generator.llm.select_components = MagicMock(return_value=([], [], []))

result = executor.execute_query("I need an AI server")
print(result)
