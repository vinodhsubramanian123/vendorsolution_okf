# Graph Report - tests  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 72 nodes · 74 edges · 11 communities (6 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 661 input · 32 output

## Graph Freshness
- Built from commit: `422dd814`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Foundation Layer Tests
- Graph Construction and Filtering
- Ontology and Knowledge Models
- TestFuzzyMatching
- TestCategoryLimits
- TestIngestion
- test_mcp_integration.py
- TestTopology

## God Nodes (most connected - your core abstractions)
1. `TestGraphBuilder` - 13 edges
2. `TestOntologyModels` - 6 edges
3. `TestOKFWriter` - 6 edges
4. `TestFuzzyMatching` - 5 edges
5. `TestCategoryLimits` - 4 edges
6. `TestIngestion` - 4 edges
7. `temp_dir()` - 2 edges
8. `TestOKFReader` - 2 edges
9. `TestRepoManager` - 2 edges
10. `test_mcp_server_parameters()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (11 total, 5 thin omitted)

### Community 0 - "Foundation Layer Tests"
Cohesion: 0.13
Nodes (7): Regression tests for IKP V1.0 Phase 1 — Foundation Layer.  Tests: 1. Ontology mo, Write an object, read it back, verify key fields match., Create a temporary directory for test artifacts., temp_dir(), TestOKFReader, TestOKFWriter, TestRepoManager

### Community 2 - "Ontology and Knowledge Models"
Cohesion: 0.20
Nodes (5): Blueprint 04 §5: Source must have permanent identity with full metadata., Blueprint 02 §7: Knowledge Delta with changes list., Blueprint 05 §13: Solution must include reasoning and confidence., Blueprint 03 §8: Rule must expose scope, confidence, evidence, version., TestOntologyModels

### Community 6 - "test_mcp_integration.py"
Cohesion: 0.40
Nodes (4): Mock the MCP ClientSession to verify initialization logic., Verify MCP Server Parameters can be constructed for the seekstone tool., test_mcp_client_init(), test_mcp_server_parameters()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestGraphBuilder` connect `Graph Construction and Filtering` to `Foundation Layer Tests`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `TestOntologyModels` connect `Ontology and Knowledge Models` to `Foundation Layer Tests`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Should `Foundation Layer Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._