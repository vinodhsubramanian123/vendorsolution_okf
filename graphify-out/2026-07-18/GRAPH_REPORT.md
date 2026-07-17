# Graph Report - vendorsolution_okf  (2026-07-17)

## Corpus Check
- 66 files · ~40,995 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16 nodes · 11 edges · 6 communities (2 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `52ac255d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- IKP Platform State
- Vendorsolution OKF
- Cross-Platform Toolchain Setup
- agy
- pip
- python

## God Nodes (most connected - your core abstractions)
1. `Vendorsolution OKF` - 3 edges
2. `Cross-Platform Toolchain Setup` - 3 edges
3. `IKP Platform State` - 3 edges
4. `1. Add `tools/` to your PATH` - 1 edges
5. `2. Frontend (ikp_web)` - 1 edges
6. `Agent Configuration` - 1 edges
7. `Knowledge Graph Statistics` - 1 edges
8. `Objects by Type` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (6 total, 4 thin omitted)

### Community 0 - "IKP Platform State"
Cohesion: 0.50
Nodes (3): IKP Platform State, Knowledge Graph Statistics, Objects by Type

### Community 2 - "Cross-Platform Toolchain Setup"
Cohesion: 0.67
Nodes (3): 1. Add `tools/` to your PATH, 2. Frontend (ikp_web), Cross-Platform Toolchain Setup

## Knowledge Gaps
- **5 isolated node(s):** `1. Add `tools/` to your PATH`, `2. Frontend (ikp_web)`, `Agent Configuration`, `Knowledge Graph Statistics`, `Objects by Type`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vendorsolution OKF` connect `Vendorsolution OKF` to `Cross-Platform Toolchain Setup`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `Cross-Platform Toolchain Setup` connect `Cross-Platform Toolchain Setup` to `Vendorsolution OKF`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **What connects `1. Add `tools/` to your PATH`, `2. Frontend (ikp_web)`, `Agent Configuration` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._