# 05. Engineering Reasoning & Solution Synthesis

---

# 1. Purpose

This blueprint defines how IKP transforms engineering knowledge into validated customer solutions.

The objective is not to search documents.

The objective is to reason over engineering knowledge in the same manner as an experienced infrastructure solution architect.

Engineering reasoning is the core business capability of IKP.

---

# 2. Engineering Philosophy

Customers rarely ask for products.

Customers describe:

* Business problems
* Workloads
* Technical objectives
* Constraints
* Budget
* Existing environment
* Growth expectations
* Compliance requirements

The implementation SHALL convert these into engineering requirements before searching the knowledge repository.

---

# 3. Solution Engineering Lifecycle

```text
Customer Request

↓

Intent Understanding

↓

Requirement Extraction

↓

Requirement Classification

↓

Metadata Filtering

↓

Knowledge Discovery

↓

Engineering Reasoning

↓

Candidate Solution Generation

↓

Compatibility Validation

↓

Optimization

↓

Multiple Solution Options

↓

Vendor Validation

↓

Engineering Explanation

↓

Knowledge Learning
```

Every recommendation SHALL follow this lifecycle.

---

# 4. Customer Requirement Understanding

Customer requests SHALL be converted into structured engineering requirements.

Examples include:

Business Requirements

* Reduce cost
* Increase performance
* AI readiness
* Future growth
* Business continuity

Technical Requirements

* Capacity
* Performance
* Availability
* Security
* Protocols
* Hypervisor
* Database
* Backup

Operational Requirements

* Existing infrastructure
* Existing vendor
* Existing licenses
* Existing support contracts

Commercial Requirements

* Budget
* Preferred vendor
* Expansion strategy
* Procurement constraints

---

# 5. Requirement Normalization

Requirements SHALL be converted into canonical engineering attributes.

Example

Customer says

> "Fast storage for AI"

Normalized Engineering Intent

* Workload = AI
* Priority = Performance
* Storage = High Performance
* GPU = Likely Required
* Low Latency = Preferred
* High Bandwidth = Required

The implementation SHALL reason using normalized engineering intent.

---

# 6. Metadata Filtering

Before reasoning begins, the implementation SHALL reduce the engineering search space.

Filtering MAY include:

* Solution Domain
* Vendor
* Product Family
* Generation
* Workloads
* Performance Class
* Capacity Class
* Availability
* Protocols
* Certifications
* Lifecycle Status

Metadata SHALL improve efficiency.

Metadata SHALL NOT determine recommendations.

---

# 7. Engineering Reasoning

After discovery, the implementation SHALL evaluate candidate knowledge using engineering reasoning.

Engineering reasoning SHALL evaluate:

Capabilities

↓

Rules

↓

Dependencies

↓

Constraints

↓

Relationships

↓

Compatibility

↓

Workloads

↓

Evidence

↓

Confidence

Every recommendation SHALL be explainable.

### 7.1 Workflow Orchestration (LangGraph)
The implementation SHALL NOT use linear execution scripts. It MUST use an Agentic State Machine (e.g., **LangGraph**) to orchestrate the engineering reasoning lifecycle.
1. **Workflow State**: The pipeline MUST maintain a structured, immutable state object (e.g. `WorkflowState`) tracking customer intent, current BOM draft, missing components, validation errors, and retry attempts.
2. **Conditional Routing**: Nodes MUST NOT hardcode next steps. The pipeline MUST use conditional edges (e.g., `should_loop_bom`) to evaluate the state dynamically and route back to drafting, to validation, or to human fallback.
3. **Bounded Retries**: To prevent infinite autonomous loops during complex engineering conflict resolution, the state machine MUST enforce strict retry limits (`attempt_count < max_attempts`). Once limits are exceeded, the workflow MUST cleanly route to a `human_intervention` node to safely halt execution without destroying progress.

---

# 8. Knowledge Graph Traversal

The implementation SHALL traverse engineering relationships rather than isolated documents.

Example

Customer requires

GPU Cluster

The implementation SHALL automatically evaluate:

GPU

↓

Supported Platform

↓

Supported Chassis

↓

CPU Compatibility

↓

Memory Rules

↓

Power Requirements

↓

Cooling Requirements

↓

Networking Requirements

↓

Firmware Requirements

↓

Software Requirements

↓

Validated Configurations

Engineering reasoning SHALL use relationships rather than keyword matching.

### 8.1 Semantic Fallback & Score Normalization
When strict relationships are missing, the implementation SHALL fallback to semantic approximation with strict numeric boundaries:
- **Score Normalization**: Vector distance scores MUST be linearly normalized (e.g. `max(0, 1 - d/2)`) rather than compressed via asymptotic formulas (like `1/(1+d)`) to ensure the difference between near-perfect matches and average matches remains mathematically significant to the UI and reasoning engine.
- **Dynamic Semantic Thresholds**: To prevent false positives, semantic similarity thresholds SHALL be dynamic based on the string length. Very short strings (e.g., SKUs <= 10 characters) MUST have a lower acceptance threshold (e.g., 0.55) to account for extreme lexical density, while longer descriptive strings MUST use a stricter threshold (e.g., 0.80).

---

# 9. Compatibility Evaluation

Every proposed solution SHALL be evaluated for compatibility.

Examples include:

Hardware Compatibility

Firmware Compatibility

Software Compatibility

Licensing Compatibility

Generation Compatibility

Expansion Compatibility

Protocol Compatibility

Operational Compatibility

Compatibility SHALL be evidence based.

---

# 10. Candidate Solution Generation

The implementation SHALL generate multiple candidate solutions.

Candidate generation SHALL balance:

Capabilities

Performance

Capacity

Availability

Expandability

Supportability

Cost

Risk

Engineering Confidence

Candidate generation SHALL not stop after the first valid solution.

---

# 11. Solution Optimization

The implementation SHALL optimize solutions according to customer priorities.

Example optimization profiles include:

Lowest Cost

Balanced

Maximum Performance

Maximum Capacity

Low Latency

AI Optimized

Database Optimized

Backup Optimized

Future Growth

Energy Efficient

Additional optimization profiles MAY be introduced without architectural changes.

---

# 12. Vendor Validation

Every candidate solution SHOULD be validated against vendor systems whenever available.

Validation SHALL identify:

Configuration Errors

Missing Components

Dependency Violations

Compatibility Problems

Licensing Issues

Firmware Issues

Portal Recommendations

Validation feedback SHALL become Knowledge Delta.

---

# 13. Recommendation Output

Every recommendation SHALL include:

Recommended Solution

Alternative Solutions

Engineering Reasoning

Capabilities Satisfied

Requirements Satisfied

Trade-offs

Dependencies

Constraints

Confidence

Supporting Evidence

Validation Status

Estimated Risks

The recommendation SHALL be understandable by both engineers and future AI systems.

---

# 14. Continuous Improvement

Every completed engineering engagement SHALL improve future recommendations.

Learning inputs include:

Portal Validation

Customer Decisions

Human Corrections

Deployment Success

Deployment Failures

Updated Vendor Knowledge

Engineering Reviews

Only validated learning SHALL update canonical engineering knowledge.

---

# 15. Acceptance Criteria

A compliant implementation SHALL:

* Understand customer intent.
* Convert business requirements into engineering requirements.
* Discover relevant engineering knowledge.
* Reason over relationships rather than documents.
* Respect rules, dependencies and constraints.
* Generate multiple valid solution options.
* Optimize recommendations according to customer priorities.
* Validate solutions using vendor systems.
* Explain every recommendation with supporting evidence.
* Learn from every validated engineering outcome.

The output of this blueprint SHALL be multiple explainable, configurable and continuously improving engineering solutions rather than simple search results.

---

# End of Blueprint 05