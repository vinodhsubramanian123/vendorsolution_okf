---
description: "GraphBuilder field mapping rules — prevents the recurring 'silently dropped field' bug class"
---

# GraphBuilder Field Serialization

## The bug pattern (happened 3 times — read this before touching `add_concept`)

`GraphBuilder.add_concept()` used to build `node_attrs` from a hand-maintained
list of `hasattr(obj, "some_field")` checks — effectively an allowlist that a
human had to remember to update every time a new field was added to any
ontology model in `ikp_platform/core/ontology/models.py`. That allowlist
silently fell out of sync **three separate times**:

1. `description` / `applicable_objects` dropped — fixed by ADR-001
   (`IKP/standards/09_ARCHITECTURE_DECISIONS_AND_EVOLUTION.md`).
2. `target_subcategory` / `component_subcategory` / `inclusive_qty` dropped —
   fixed by commit `a6ef5df`, which meant every `CategoryLimit` rule silently
   evaluated against zero items instead of the real count.
3. `platform_id` dropped — found during the 2026-07-18 audit. This one is the
   most insidious of the three: it didn't throw an error or produce an empty
   result, it silently broke the Rule dedup check in `RepoManager.add_concept`
   (`data.get("platform_id") == obj.platform_id` could never be true), so
   duplicate rules quietly piled up instead of being merged.

Every one of these took a separate debugging session (or a live-audit
discovery) to find, because the failure mode is never a crash — it's a
correct-looking graph with a `None` where a real value should be, which only
shows up later as "the rule engine isn't catching this constraint" or
"duplicates in the repository."

## The fix (as of 2026-07-18) — DO NOT reintroduce the allowlist pattern

`add_concept` now builds `node_attrs` from `obj.model_dump(mode="json",
exclude={"attributes", "relationships", "history"})` — i.e. it dumps
*every* field on the Pydantic model automatically, then layers a small,
explicit set of transformations on top for fields that need to be flattened
or aliased (structured `attributes` → `attr_<name>` keys,
`performance_requirements`/`capacity_requirements` → `req_perf_*`/`req_cap_*`
keys, and a short list of historical `attr_*` aliases). See the docstring on
`GraphBuilder.add_concept` for the exact current list.

**Rule:** If you add a new field to any `BaseEngineeringObject` subclass in
`models.py`, you do **not** need to touch `GraphBuilder.add_concept` for it to
reach the graph — it will, automatically, under its own field name. You only
need to touch `add_concept` if the new field needs a *different* key name in
`node_attrs` than its Pydantic field name (i.e. it needs a flatten/alias, like
`performance_requirements` does).

**Rule:** Never add a `hasattr(obj, "...")` conditional back into
`add_concept` as a way to "just add one more field." That's exactly the
pattern that caused all three bugs above. If you think you need one, you're
almost certainly looking for the alias/flatten list instead.

**Rule:** `tests/test_graph_field_parity.py` is the regression guard for this
whole bug class. It doesn't hardcode field names to check — it walks
`type(obj).model_fields` for `Rule`, `CategoryLimit`, `Component`, `SKU`,
`Workload`, and `Platform`, and asserts every field is reachable in
`node_attrs`. **Any new ontology object type (e.g. if `Variant` or
`Configuration` extraction gets built out — see Gap 23 in the phase-2 audit)
should get its own test function added to that file**, following the same
pattern: construct an instance with every field populated with a real value,
add it to an `empty_graph`, call `_assert_every_field_reachable`.

## Same principle applies to `OKFWriter._generate_frontmatter`

`okf_writer.py`'s `_generate_frontmatter` still uses the old
`hasattr`-conditional pattern (it predates this fix and wasn't in scope for
the 2026-07-18 change). It hasn't caused a *known* bug yet, but it's the same
shape of risk: a field added to a model won't automatically show up in the
OKF frontmatter unless someone remembers to add an `if hasattr(obj, "x") and
obj.x: fm["x"] = obj.x` line. If you're doing further ontology work, consider
applying the same `model_dump`-based fix there, with the same test-per-object-type
pattern in `tests/test_foundation.py`'s OKF round-trip tests.
