# Graph Report - repository  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 22 nodes · 25 edges · 5 communities (4 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.9)
- Token cost: 282 input · 16 output

## Graph Freshness
- Built from commit: `422dd814`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Server Hardware Components
- HPE ProLiant DL380 Gen12 Engineering Rules Index
- Repository Update Log
- AI and Machine Learning
- DIMM Slot Count

## God Nodes (most connected - your core abstractions)
1. `HPE ProLiant DL380 Gen12` - 12 edges
2. `Repository Update Log` - 7 edges
3. `HPE ProLiant DL380 Gen12 Engineering Rules Index` - 5 edges
4. `AI and Machine Learning` - 3 edges
5. `Engineering Rule 1` - 3 edges
6. `2200W Power Supply` - 2 edges
7. `NVIDIA H200 NVL 141GB` - 2 edges
8. `Engineering Rule 10` - 2 edges
9. `Engineering Rule 70` - 2 edges
10. `Maximum Memory Capacity Constraint` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Repository Update Log` --references--> `HPE ProLiant DL380 Gen12`  [EXTRACTED]
  log.md → compute/proliant/gen12/hpe-proliant-dl380-gen12.md
- `Repository Update Log` --references--> `NVIDIA H200 NVL 141GB`  [EXTRACTED]
  log.md → compute/proliant/gen12/hpe-proliant-dl380-gen12/components/gpu/hpe-proliant-dl380-gen12-components-gpu-h200-nvl.md
- `Repository Update Log` --references--> `2200W Power Supply`  [EXTRACTED]
  log.md → compute/proliant/gen12/hpe-proliant-dl380-gen12/components/psu/hpe-proliant-dl380-gen12-components-psu-2200w.md
- `Repository Update Log` --references--> `Maximum Memory Capacity Constraint`  [EXTRACTED]
  log.md → compute/proliant/gen12/hpe-proliant-dl380-gen12/constraints/hpe-proliant-dl380-gen12-constraints-max-memory.md
- `Repository Update Log` --references--> `Engineering Rule 1`  [EXTRACTED]
  log.md → compute/proliant/gen12/hpe-proliant-dl380-gen12/rules/hpe-proliant-dl380-gen12-rules-rule-001.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **HPE ProLiant DL380 Gen12 Ecosystem** — compute_proliant_gen12_hpe_proliant_dl380_gen12, compute_proliant_gen12_hpe_proliant_dl380_gen12_components_psu_2200w, compute_proliant_gen12_hpe_proliant_dl380_gen12_rules_rule_001, compute_proliant_gen12_hpe_proliant_dl380_gen12_constraints_max_memory [INFERRED 0.85]
- **HPE ProLiant DL380 Gen12 Platform Ecosystem** — compute_proliant_gen12_hpe_proliant_dl380_gen12, compute_proliant_gen12_hpe_proliant_dl380_gen12_processors_xeon_6505p, compute_proliant_gen12_hpe_proliant_dl380_gen12_components_gpu_h200_nvl, compute_proliant_gen12_hpe_proliant_dl380_gen12_constraints_dimm_slots [INFERRED 0.90]
- **DL380 Gen12 Engineering Rules** — compute_proliant_gen12_hpe_proliant_dl380_gen12_rules_rule_010, compute_proliant_gen12_hpe_proliant_dl380_gen12_rules_rule_070, compute_proliant_gen12_hpe_proliant_dl380_gen12_rules_rule_074 [INFERRED 0.80]

## Communities (5 total, 1 thin omitted)

### Community 0 - "Server Hardware Components"
Cohesion: 0.29
Nodes (7): HPE ProLiant DL380 Gen12, OCP 3.0 Network Adapter Slot, P03178-B21, P25527-B21, P36394-B21, 1000W Power Supply, Intel Xeon 6 6505P

### Community 1 - "HPE ProLiant DL380 Gen12 Engineering Rules Index"
Cohesion: 0.33
Nodes (6): HPE ProLiant DL380 Gen12 Engineering Rules Index, Engineering Rule 1, Engineering Rule 10, Engineering Rule 15, Engineering Rule 70, Engineering Rule 74

### Community 2 - "Repository Update Log"
Cohesion: 0.40
Nodes (5): NVIDIA H200 NVL 141GB, 2200W Power Supply, Maximum Memory Capacity Constraint, Intel Xeon 6 6788P, Repository Update Log

### Community 3 - "AI and Machine Learning"
Cohesion: 0.67
Nodes (3): Workload Index, AI and Machine Learning, HPE ProLiant DL380 Gen12

## Knowledge Gaps
- **13 isolated node(s):** `Maximum Memory Capacity Constraint`, `Intel Xeon 6 6788P`, `P03178-B21`, `P25527-B21`, `P36394-B21` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HPE ProLiant DL380 Gen12` connect `Server Hardware Components` to `HPE ProLiant DL380 Gen12 Engineering Rules Index`, `Repository Update Log`?**
  _High betweenness centrality (0.583) - this node is a cross-community bridge._
- **Why does `Repository Update Log` connect `Repository Update Log` to `Server Hardware Components`, `HPE ProLiant DL380 Gen12 Engineering Rules Index`, `AI and Machine Learning`?**
  _High betweenness centrality (0.405) - this node is a cross-community bridge._
- **What connects `Maximum Memory Capacity Constraint`, `Intel Xeon 6 6788P`, `P03178-B21` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._