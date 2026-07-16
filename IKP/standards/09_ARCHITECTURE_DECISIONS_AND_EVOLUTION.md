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

Final Principle

IKP is not a document repository.

IKP is not a search engine.

IKP is not a chatbot.

IKP is an Engineering Knowledge Platform that continuously acquires, understands, organizes, reasons over, validates and learns from engineering knowledge to produce explainable infrastructure solutions.

Everything implemented within IKP SHALL support that objective.