---
description: "Relationship edges have inconsistent direction across the codebase — always query both ways unless you've confirmed otherwise"
---

# Relationship Edge Direction

`EngineeringRelationship` edges are directed (`source -> target` in the
NetworkX graph), but **different extractors and tests orient structural
relationships (especially `Contains`) differently.** Some code adds
`platform -> component` ("platform Contains component"); other code adds
`component -> platform` ("component Contains-relationship-pointing-at
platform", used when the component is extracted first and the platform
isn't known yet). There is currently no enforced canonical direction for
`Contains`.

This has caused the same bug twice:

1. `RuleEngine._evaluate_constraints` originally looked for constraints only
   via outbound `platform -> constraint` edges, but extractors/tests
   frequently add `constraint -> platform` instead. Fixed in commit
   `a6ef5df` by scanning `direction="both"` and taking whichever side isn't
   the platform.
2. `RuleEngine._check_compatibility` had the exact same bug in a different
   method (`traverse_relationships(platform_id, "Contains", "outbound")` for
   checking whether a component belongs to a platform) — found and fixed
   during the 2026-07-18 audit, using the same `direction="both"` pattern.

**Rule:** When traversing a relationship type whose direction isn't
explicitly pinned down by a Blueprint or by `EngineeringRelationship`'s own
semantics (`Requires`, `Depends On`, `Compatible With` are inherently
symmetric-ish and mostly already handled via `direction="both"` in
`GraphBuilder.get_compatible`/`get_dependencies`) — default to
`direction="both"` and resolve which side is the node you started from,
rather than assuming `outbound`. Only use a single fixed direction if you've
confirmed (by grepping every call site that constructs that relationship
type) that it's always added the same way.

**Longer-term fix worth doing, not yet done:** rather than relying on every
call site to remember `direction="both"`, consider adding a
`GraphBuilder.get_related(node_id, relationship_type)` helper that always
searches both directions and returns "the other node" directly (this is
exactly the pattern `get_compatible` already implements for
`Compatible With` — the same helper shape should be reused for `Contains`
instead of hand-rolling the both-directions-then-pick-the-other-side logic
at each call site). If you're doing further RuleEngine work, extracting this
helper is a good opportunity to close the whole class of bug at once, the
same way the `graph_serialization.md` fix did for field-dropping.
