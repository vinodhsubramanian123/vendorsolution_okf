# Graph Report - ikp_web  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 106 nodes · 96 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 424 input · 144 output

## Graph Freshness
- Built from commit: `422dd814`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- App TypeScript Config
- Node TypeScript Config
- Linting and React Rules
- Development Dependencies
- Project Scripts and Metadata
- Application Dependencies
- Build Plugins and Documentation
- TypeScript Library Targets
- Root TypeScript Config
- HTML Entry Point
- Icon Assets
- Illustration Assets
- React Brand Assets
- Vite Brand Assets

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `compilerOptions` - 15 edges
3. `scripts` - 5 edges
4. `plugins` - 4 edges
5. `react` - 3 edges
6. `rules` - 3 edges
7. `lib` - 3 edges
8. `react/only-export-components` - 2 edges
9. `axios` - 2 edges
10. `lucide-react` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Vite React Stack** — vite_plugin_react, vite_plugin_react_swc, oxlint, react_compiler [INFERRED 0.80]

## Communities (15 total, 6 thin omitted)

### Community 0 - "App TypeScript Config"
Cohesion: 0.10
Nodes (20): src, vite/client, compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, module (+12 more)

### Community 1 - "Node TypeScript Config"
Cohesion: 0.10
Nodes (19): node, vite.config.ts, compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection (+11 more)

### Community 2 - "Linting and React Rules"
Cohesion: 0.15
Nodes (10): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, react, typescript (+2 more)

### Community 3 - "Development Dependencies"
Cohesion: 0.15
Nodes (13): devDependencies, @types/node, @types/react, @types/react-dom, typescript, vite, @vitejs/plugin-react, @types/node (+5 more)

### Community 4 - "Project Scripts and Metadata"
Cohesion: 0.20
Nodes (9): name, private, scripts, build, dev, lint, preview, type (+1 more)

### Community 5 - "Application Dependencies"
Cohesion: 0.22
Nodes (9): axios, lucide-react, dependencies, axios, lucide-react, react, react-dom, react (+1 more)

### Community 6 - "Build Plugins and Documentation"
Cohesion: 0.33
Nodes (5): Oxlint, oxlint, React Compiler, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 7 - "TypeScript Library Targets"
Cohesion: 0.67
Nodes (3): DOM, lib, ES2023

## Knowledge Gaps
- **68 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+63 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `devDependencies` connect `Development Dependencies` to `Project Scripts and Metadata`, `Build Plugins and Documentation`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `dependencies` connect `Application Dependencies` to `Project Scripts and Metadata`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `compilerOptions` connect `App TypeScript Config` to `TypeScript Library Targets`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **What connects `$schema`, `typescript`, `oxc` to the rest of the system?**
  _68 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `App TypeScript Config` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `Node TypeScript Config` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._