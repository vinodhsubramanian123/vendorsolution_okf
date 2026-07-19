"""
Regression guard for the "GraphBuilder silently drops a field" bug class.

History: `GraphBuilder.add_concept` used to build `node_attrs` from a
hand-maintained list of `hasattr(...)` checks. As the ontology grew, that
allowlist fell out of sync with the actual Pydantic models THREE separate
times:

  1. `description` / `applicable_objects` were dropped -- fixed by ADR-001
     (IKP/standards/09_ARCHITECTURE_DECISIONS_AND_EVOLUTION.md).
  2. `target_subcategory` / `component_subcategory` / `inclusive_qty` were
     dropped -- fixed by commit a6ef5df ("CategoryLimit Serialization
     Issue"), which caused CategoryLimit rules to always evaluate against
     zero items.
  3. `platform_id` was found still-missing during the 2026-07-18 audit. This
     silently broke the Rule dedup check in `RepoManager.add_concept`
     (`data.get("platform_id") == obj.platform_id` could never match).

`add_concept` was refactored to build `node_attrs` from `obj.model_dump()`
instead of an allowlist, which closes this bug class structurally rather
than field-by-field. This test is the regression guard: it doesn't hardcode
specific field names to check (that's exactly the pattern that already
failed three times) -- it walks every field actually defined on each
ontology model and asserts each one reaches `node_attrs`, either directly or
via one of the small set of documented `attr_*`/`req_*` aliases.

If this test starts failing, the most likely cause is that someone
reintroduced a manual allowlist (or an `exclude=...` that's too broad) in
`GraphBuilder.add_concept`. See .agents/rules/graph_serialization.md.
"""
from datetime import datetime, timezone

from ikp_platform.core.repository.graph_builder import GraphBuilder
from ikp_platform.core.ontology.models import (
    Rule,
    RuleSeverity,
    ConfidenceLevel,
    CategoryLimit,
    Workload,
    Platform,
    Component,
    SKU,
    PackagingType,
    LifecycleStatus,
    EngineeringAttribute,
    EvidenceRecord,
)

# Fields intentionally NOT expected as a flat/aliased key in node_attrs,
# because add_concept handles them via a documented, different mechanism.
HANDLED_SEPARATELY = {"attributes", "relationships", "history", "id"}

# field_name -> the alternate key it's expected under in node_attrs, for the
# handful of fields kept under a historical `attr_*`/`req_*` alias.
ALIASES = {
    "component_category": "attr_component_category",
    "component_subcategory": "attr_component_subcategory",
    "inclusive_qty": "attr_inclusive_qty",
    "target_category": "attr_target_category",
    "target_subcategory": "attr_target_subcategory",
    "part_number": "attr_part_number",
}


def _assert_every_field_reachable(obj, node_attrs: dict):
    """Walk every Pydantic field on `obj` and confirm it made it into
    node_attrs, either under its own name or a documented alias."""
    expected = obj.model_dump(mode="json")

    missing = []
    for field_name in type(obj).model_fields:
        if field_name in HANDLED_SEPARATELY:
            continue

        key = ALIASES.get(field_name, field_name)
        if key not in node_attrs:
            missing.append(f"{field_name!r} (expected under node_attrs[{key!r}])")
            continue

        # performance_requirements / capacity_requirements are flattened
        # into req_perf_*/req_cap_* keys rather than kept as a single dict --
        # spot-check flattening happened instead of an exact-value compare.
        if field_name in ("performance_requirements", "capacity_requirements"):
            prefix = "req_perf_" if field_name == "performance_requirements" else "req_cap_"
            for sub_key in expected[field_name]:
                if f"{prefix}{sub_key}" not in node_attrs:
                    missing.append(f"{field_name}.{sub_key} (expected under node_attrs[{prefix}{sub_key!r}])")
            continue

        assert node_attrs[key] == expected[field_name], (
            f"node_attrs[{key!r}] = {node_attrs[key]!r}, "
            f"but {type(obj).__name__}.{field_name} = {expected[field_name]!r}"
        )

    assert not missing, (
        f"{type(obj).__name__}: the following fields never reached node_attrs: "
        + ", ".join(missing)
    )


def test_rule_fields_all_reach_graph(empty_graph):
    """Covers the exact fields ADR-001 fixed, plus every other Rule field."""
    rule = Rule(
        id="rule/test-full",
        title="Test Rule With Every Field Set",
        description="A rule constructed with every field populated.",
        vendor="HPE",
        solution_domain="Compute",
        product_family="ProLiant",
        generation="Gen12",
        platform_id="hpe-proliant-dl380-gen12",
        lifecycle_status=LifecycleStatus.ACTIVE,
        capabilities=["ai"],
        tags=["gpu"],
        scope="platform",
        severity=RuleSeverity.CRITICAL,
        confidence=ConfidenceLevel.HIGH,
        applicable_objects=["hpe-proliant-dl380-gen12/components/p12345"],
        trigger_conditions=["More than 4 GPUs selected"],
        expected_outcome="Reject the configuration.",
        version=2,
        negated=False,
        scaling_factor="per-slot",
        dependency_targets=["hpe-proliant-dl380-gen12/components/psu"],
        evidence=[EvidenceRecord(source_id="SRC-1", confidence=ConfidenceLevel.HIGH)],
    )
    empty_graph.add_concept(rule)
    node_attrs = empty_graph.graph.nodes[rule.id]
    _assert_every_field_reachable(rule, node_attrs)


def test_category_limit_fields_all_reach_graph(empty_graph):
    """Covers the exact fields commit a6ef5df fixed (target_subcategory,
    component_subcategory, inclusive_qty), plus every other field."""
    limit = CategoryLimit(
        id="limit/test-full",
        title="Max OCP Slots",
        platform_id="hpe-proliant-dl380-gen12",
        limit_name="Max OCP Slots",
        limit_value=2,
        limit_unit="slots",
        target_category="Infrastructure",
        target_subcategory="Riser",
    )
    empty_graph.add_concept(limit)
    node_attrs = empty_graph.graph.nodes[limit.id]
    _assert_every_field_reachable(limit, node_attrs)


def test_component_fields_all_reach_graph(empty_graph):
    component = Component(
        id="component/test-full",
        title="Test GPU",
        platform_id="hpe-proliant-dl380-gen12",
        component_category="GPU",
        component_subcategory="Accelerator",
        packaging_type=PackagingType.BUNDLE,
        inclusive_qty=1,
        attributes=[EngineeringAttribute(name="TDP", value=700, unit="W")],
    )
    empty_graph.add_concept(component)
    node_attrs = empty_graph.graph.nodes[component.id]
    _assert_every_field_reachable(component, node_attrs)
    assert node_attrs["attr_tdp"] == 700


def test_sku_fields_all_reach_graph(empty_graph):
    sku = SKU(
        id="sku/test-full",
        title="P12345-B21",
        platform_id="hpe-proliant-dl380-gen12",
        part_number="P12345-B21",
        price=1999.0,
        currency="USD",
        packaging_type=PackagingType.SPARE,
        inclusive_qty=1,
        component_id="component/test-full",
    )
    empty_graph.add_concept(sku)
    node_attrs = empty_graph.graph.nodes[sku.id]
    _assert_every_field_reachable(sku, node_attrs)


def test_workload_requirement_dicts_flatten_into_graph(empty_graph):
    """Workload requirements are flattened rather than kept as nested dicts
    -- confirms the flattening actually happens, not just that the raw dict
    is present somewhere."""
    workload = Workload(
        id="workload/test-full",
        title="AI Training",
        performance_requirements={"gpu_count": 8, "interconnect": "nvlink"},
        capacity_requirements={"memory_gb": 512},
    )
    empty_graph.add_concept(workload)
    node_attrs = empty_graph.graph.nodes[workload.id]
    _assert_every_field_reachable(workload, node_attrs)
    assert node_attrs["req_perf_gpu_count"] == 8
    assert node_attrs["req_cap_memory_gb"] == 512


def test_platform_fields_all_reach_graph(empty_graph):
    platform = Platform(
        id="hpe-proliant-dl380-gen12",
        title="HPE ProLiant DL380 Gen12",
        vendor="HPE",
        solution_domain="Compute",
        product_family="ProLiant",
        generation="Gen12",
        parent_platform_id="hpe-proliant-dl380-gen12-enclosure",
        variants=["hpe-proliant-dl380-gen12/variants/sff"],
        slot_mapping_ids=["hpe-proliant-dl380-gen12/slots/mezz1"],
        platform_sku="P12345-B21",
    )
    empty_graph.add_concept(platform)
    node_attrs = empty_graph.graph.nodes[platform.id]
    _assert_every_field_reachable(platform, node_attrs)


def test_compatibility_check_finds_reverse_direction_contains_edge(empty_graph):
    """Regression test for the direction-assumption bug found alongside the
    field-parity issues during the 2026-07-18 audit (see
    .agents/rules/relationship_direction.md). _check_compatibility used to
    only look for outbound platform->component 'Contains' edges; if an
    extractor added the edge the other way (component->platform), the
    component was wrongly flagged as having no compatibility link even
    though a Contains relationship genuinely existed."""
    from ikp_platform.core.reasoning.rule_engine import RuleEngine
    from ikp_platform.core.ontology.models import (
        Platform,
        Component,
        EngineeringRelationship,
        RelationshipType,
    )

    platform = Platform(id="platform/x", title="Platform X", solution_domain="Compute")
    # Edge deliberately points component -> platform, the "wrong" direction
    # relative to what _check_compatibility used to assume.
    component = Component(
        id="component/y",
        title="Component Y",
        solution_domain="Compute",
        relationships=[
            EngineeringRelationship(target_id=platform.id, relationship_type=RelationshipType.CONTAINS)
        ],
    )

    empty_graph.add_concept(platform)
    empty_graph.add_concept(component)

    engine = RuleEngine(empty_graph)
    reasoning_chain: list = []
    errors = engine._check_compatibility(platform.id, [component.id], reasoning_chain)

    assert errors == []
    assert not any("no explicit compatibility link" in line for line in reasoning_chain)


def test_platform_id_survives_for_rule_dedup(empty_graph):
    """Direct regression test for the specific dedup bug found in the
    2026-07-18 audit: RepoManager.add_concept compares
    data.get('platform_id') == obj.platform_id to detect semantic
    duplicates within the same platform. That comparison is meaningless if
    platform_id never reaches node_attrs in the first place."""
    rule = Rule(id="rule/dedup-check", title="x", platform_id="hpe-dl380-gen12")
    empty_graph.add_concept(rule)
    assert empty_graph.graph.nodes[rule.id].get("platform_id") == "hpe-dl380-gen12"
