09. Architecture Decisions & Evolution
1. Purpose

This blueprint defines how the IKP architecture evolves over time.

The objective is to ensure that the platform continuously gains engineering knowledge while maintaining a stable architecture.

Architecture changes should be rare.

Knowledge changes should be continuous.

2. Core Principle

Architecture is stable. Knowledge evolves. Intelligence improves.

This principle governs every future change to IKP.

3. Architectural Stability

The following concepts are considered architectural foundations and SHALL remain stable unless a fundamental design limitation is discovered.

Engineering Knowledge Platform philosophy
Canonical Engineering Ontology
Knowledge Acquisition Pipeline
Engineering Reasoning Model
Canonical Repository Model
Validation and Learning Lifecycle
Engineering Explainability
Knowledge Integrity

Future work SHALL extend these foundations rather than replace them.

4. Knowledge Evolution

Engineering knowledge is expected to change continuously.

Examples include:

New vendors
New product families
New generations
New firmware
New software
New protocols
New workloads
New certifications
New engineering rules
New dependencies
New validation logic
New engineering best practices

These changes SHALL be incorporated through Knowledge Deltas.

Architecture SHALL remain unchanged.

5. Architecture Decision Records (ADR)

Architectural changes SHALL be documented through Architecture Decision Records.

Every ADR SHALL include:

Decision ID
Date
Problem Statement
Alternatives Considered
Decision
Impact
Migration Strategy
Approval

Knowledge updates SHALL NOT require ADRs.

Only architectural changes require ADRs.

6. Extension Philosophy

The platform SHALL be extensible.

Examples of expected future extensions include:

New engineering domains
New document types
New portal integrations
New automation tools
New reasoning strategies
New optimization profiles
New customer industries

These SHALL integrate through ontology extensions and new knowledge rather than architectural redesign.

7. Repository Evolution

The canonical repository is expected to grow continuously.

Growth includes:

Engineering objects
Metadata
Relationships
Rules
Workloads
Evidence
Validation knowledge
Reference examples

Growth SHALL improve engineering intelligence without requiring repository redesign.

8. Reference Library Evolution

The Reference Library SHALL become one of the most valuable engineering assets.

Every significant engineering engagement SHOULD contribute new examples.

Examples include:

Successful customer solutions
Failed configurations
Portal validation scenarios
Complex dependency chains
New workloads
Cross-vendor architectures
Performance tuning scenarios
Migration scenarios

Examples improve implementation quality without changing architecture.

9. Continuous Improvement

The implementation SHOULD continuously improve:

extraction quality
metadata quality
relationship discovery
rule discovery
reasoning quality
recommendation quality
validation accuracy
engineering confidence

These improvements SHALL be driven by engineering evidence and validated learning.

10. Versioning Strategy

Two independent version streams SHALL exist.

Architecture Version

Changes only when architecture changes.

Expected frequency: rare.

Knowledge Version

Changes whenever engineering knowledge changes.

Expected frequency: continuous.

This separation prevents unnecessary architectural instability.

11. Definition of Success

The project reaches long-term success when:

New vendors require only new knowledge.
New products require only new knowledge.
New workloads require only new knowledge.
New engineering examples improve recommendations.
Repository quality continuously increases.
Engineering effort continuously decreases.
Customer solution quality continuously improves.

The architecture remains largely unchanged throughout this evolution.

## Architecture Decision Records (ADR) Log

### ADR-001: OKFWriter Path Uniqueness and String Matching Rules

**Date:** 2026-07-16
**Problem Statement:** Rules with the same generic titles ("Engineering Rule 1") extracted from different platforms within the same solution domain overwrote each other in the repository because `OKFWriter` used the title for file naming. Additionally, strict string matching for `applicable_objects` against component/platform IDs failed due to granular ID differences (e.g. `hpe-proliant-dl380-gen12` vs `hpe-proliant-dl380-gen12/components/p12345`). Finally, graph bootstrapping dropped crucial fields (`description` and `applicable_objects`) causing downstream reasoning failures.
**Decision:**
1. **Repository Serialization:** All `BaseEngineeringObject` serialization in `OKFWriter` MUST use `obj.id` exclusively for generating the filename to prevent collision. Titles shall not be used for naming.
2. **Graph Bootstrapping:** `GraphBuilder.add_concept` MUST guarantee mapping of critical rule and object fields natively defined in the Pydantic models (e.g., `applicable_objects`, `description`) to NetworkX `node_attrs`.
3. **Engineering Reasoning:** The `RuleEngine` MUST perform bidirectional substring evaluation when checking if an object applies to a rule (i.e. if `applicable_object` is a substring of `component_id` or vice versa), rather than strict exact matching.
4. **Intent Parsing:** LLM intent schemas MUST include `target_platform` to map queries strictly, and fallbacks must include programmatic heuristics matching core platform names (e.g., 'dl380', 'dl580', 'alletra').
**Impact:** Rules are deterministically persisted per-platform without collisions. Reasoning dynamically matches relevant objects despite granular suffix differences in IDs. Intent effectively routes platform-specific queries to appropriate graph clusters.
**Approval:** Approved.

### ADR-002: Explicit Graph Edge Preservation across Restarts
**Date:** 2026-07-18
**Problem Statement:** `OKFReader` was dropping `Rule` multi-line markdown bodies (which contain explicit Graph Edges) upon restart because the regex relied on `re.MULTILINE` and `$` which matched prematurely at the first newline.
**Decision:** All markdown payload regex parsers MUST use `re.DOTALL` and strict end-of-file tokens (`\Z`) to guarantee full block extraction of evidence and text-based relationship edges.
**Impact:** Prevents fatal loss of relationship graph edges on service restart. Graph states are strictly idempotent across persistence cycles.
**Approval:** Approved.

### ADR-003: Linear Score Normalization and Dynamic Thresholds for Semantic Fallbacks
**Date:** 2026-07-18
**Problem Statement:** When checking BOQs, exact ID matches often failed. The semantic fallback used asymptotic score compression (`1/(1+d)`) which washed out the difference between excellent and average matches. Furthermore, a static threshold caused false positives for dense, short strings (like SKUs).
**Decision:**
1. **Linear Normalization:** ChromaDB L2 distance MUST be linearly scalarized (`max(0, 1 - d/2)`).
2. **Dynamic Thresholds:** Semantic acceptance thresholds MUST scale with query length. Short queries (`<= 10` characters) require a looser boundary (`0.55`) to account for dense lexical differences, while long queries require a stricter boundary (`0.80`).
3. **Weight Hierarchy:** Graph validation MUST prioritize component completeness via numeric `attr_component_weight` hierarchy maps (e.g. Platform=100, CPU=90).
**Impact:** BOQ validation correctly maps mismatched SKUs (e.g., matching a bare SKU against a descriptive ID) without returning garbage false positives. Component validation can distinguish between missing accessories and missing core infrastructure.
**Approval:** Approved.

Final Principle

IKP is not a document repository.

IKP is not a search engine.

IKP is not a chatbot.

IKP is an Engineering Knowledge Platform that continuously acquires, understands, organizes, reasons over, validates and learns from engineering knowledge to produce explainable infrastructure solutions.

Everything implemented within IKP SHALL support that objective.

### ADR-004: Orchestrator Decoupling, Telemetry Injection, and E2E Testing
**Date:** 2026-07-19
**Problem Statement:** LangGraph workflow nodes and FastAPI endpoints lacked structured observability. Additionally, the `WorkflowNodes` had tightly coupled dependencies to concrete classes (e.g., `IntentParser`, `SolutionGenerator`), causing infinite LLM recursive loops during isolated CI testing due to unintentional external API quota exhaustion. 
**Decision:**
1. **Dependency Injection:** The orchestrator nodes MUST accept core reasoning engines via constructor injection (Dependency Injection pattern). Concrete execution chains MUST NOT statically import or instantiate these engines internally.
2. **Telemetry Tracing:** A universal `@telemetry_trace` decorator MUST wrap all workflow stages and API endpoints. The decorator MUST capture execution duration, exceptions, sanitized parameter payloads, and emit structured JSON compatible with standard log aggregators.
3. **E2E UI Testing:** Browser testing (e.g. Playwright) MUST run purely against the UI frontend, fully mocking the backend in scenarios where legacy partner portals are integrated, to prevent network timeouts and flaky test behavior.
**Impact:** Prevents LLM quota exhaustion in automated test pipelines by natively allowing mock objects. Granular telemetry enables precise distributed tracing of the LLM reasoning pipelines.
**Approval:** Approved.