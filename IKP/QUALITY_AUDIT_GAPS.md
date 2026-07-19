# Vendorsolution OKF Quality Audit Gaps

Audit date: 2026-07-19  
Scope: codebase, generated OKF repository state, docs, tests, scripts, frontend, backend, ingestion, reasoning, validation, workflow, and local quality gates.  
Out of scope per request: security hardening and deployment readiness.

## Executive Summary

The platform has a strong backbone: a canonical ontology, OKF reader/writer, graph bootstrap, ingestion pipeline, API, UI, and a backend suite that currently passes cleanly. The main quality risk is now concentrated in reasoning fidelity, OKF round-trip parity, and incomplete learning/review integrations. The docs and local run scripts have been synchronized with the current implementation, but several runtime capabilities are still partial or placeholder.

Priority order:

1. Fix deterministic rule evaluation so rules fail only when their actual trigger/condition is violated.
2. Make learning/review/delta flows fully persistent and path-preserving.
3. Harden ingestion fidelity and OKF round-trip parity for fields already in the ontology.
4. Improve API/frontend typed contracts, visible error states, and behavior-level UI tests.
5. Add status visibility for optional integrations such as LLM, vector index, and MCP.

## Verification Performed

- `uv run pytest -q`: passed, `54 passed, 1 warning` before dependency cleanup.
- `uv run pytest tests/test_api_endpoints.py -q`: passed, `2 passed`, no Starlette warning after adding `httpx2`.
- `npm run build --prefix ikp_web`: passed.
- `npm run lint` in `ikp_web/`: completed with warnings.
- `uv run ruff check .` / `make lint`: passed.
- `make typecheck`: available, but still a known mypy backlog rather than a clean gate.
- `uv run python -m ikp_platform.cli status`: loaded 414 objects and 339 relationships, matching `STATE.md`.
- `git diff --check`: passed.

## Critical Correctness Gaps

### 1. Rule engine treats every applicable Error/Critical rule as a violation

Evidence: `ikp_platform/core/reasoning/rule_engine.py:189-231`

The rule engine does not parse trigger conditions or expected outcomes. If a rule applies to the platform and has severity `Error` or `Critical`, it appends a violation unconditionally.

Why it matters: a rule like "Must be selected with X" should fail only when the trigger is present and X is missing. A rule like "Cannot be selected with Y" should fail only when conflicting components coexist. Current behavior creates false negatives and makes extracted rule severity dangerous.

How to fix:

- Introduce a deterministic rule evaluator for the current rule schema:
  - `REQUIRES`: if trigger object selected, dependency target must be selected.
  - `INCOMPATIBLE_WITH`: selected objects must not include target pair.
  - quantity limits should stay in `CategoryLimit`.
- Use `trigger_conditions`, `dependency_targets`, and `negated` rather than only `severity`.
- Keep unknown/unparsed rules as "noted/manual review" instead of failures.
- Add tests for satisfied require rule, missing require rule, satisfied incompatibility rule, and conflicting incompatibility rule.

### 2. Review approval may write approved objects to a new path instead of updating original file

Evidence: `ikp_platform/api.py:342-369`, `ikp_platform/core/repository/okf_writer.py:40-82`

Approval scans all objects, updates confidence, and calls `repo.add_concept(target_obj)`. It does not know the original file path. Path recomputation can differ from the original path when parser/writer fields drift, and `obj_path` is unused.

Why it matters: approving a review item can duplicate or relocate OKF content rather than update the original source of truth.

How to fix:

- Have `OKFReader` return object plus source file path, or maintain an ID-to-path index during bootstrap.
- Make `approve_object` update the exact file where the object was read.
- Add a test that approves a low-confidence object and asserts the same file path changes and no duplicate appears.

## Learning And Integration Gaps

### 3. LearningEngine is only partially connected to CLI/API review flows

Evidence: `ikp_platform/core/learning/learning_engine.py:47-99`, `ikp_platform/cli.py:229-243`

`LearningEngine` can process in-memory validated deltas, and BOQ alias correction now applies aliases for the current flow. The broader lifecycle is still incomplete: CLI `learn` only counts markdown files in `history/` and says manual review is required, and delta status/list/approve/reject/merge is not a unified persistent workflow.

Why it matters: there is no executable lifecycle from validation feedback to reviewed, merged canonical knowledge.

How to fix:

- Persist delta status as structured frontmatter and load it into `LearningEngine`.
- Add API/CLI commands to list, approve, reject, and merge deltas.
- Implement `DeltaChange` application for supported fields.
- Make "record-only delta" vs "mergeable delta" explicit in schema.

### 4. Vendor portal integration is only an interface/stub

Evidence: `ikp_platform/core/validation/validator.py:64-82`, `ikp_platform/core/workflow/nodes.py:111-124`, `CONTEXT.md`

Docs mention live partner portal dynamic validation, temporary/permanent portal errors, HITL fallback, and knowledge updates. Code returns `is_valid_dynamic=True` unconditionally and has placeholder nodes.

Why it matters: users may assume post-validation is real. The system currently cannot classify portal errors, consume portal recommendations, or update knowledge based on live validation feedback.

How to fix:

- Rename UI/docs to "manual review placeholder" until an integration exists.
- Add a concrete `VendorValidator` implementation contract with mocked adapter tests.
- Make workflow dynamic validation fail closed to "not configured" when no adapter exists, or keep it opt-in.

### 5. MCP/Obsidian integration is optional but treated as normal search path

Evidence: `SolutionGenerator` accepts `mcp_client`; `PDFExtractor` constructs `ObsidianMCPClient`; rule extraction cross-references MCP results.

Why it matters: MCP failures are mostly swallowed, which is fine for resilience, but the quality of evidence and search reduction depends on an integration whose availability is not visible in status or tests.

How to fix:

- Add `/api/status.integrations` with LLM, vector index, MCP availability.
- Add tests where MCP is unavailable and where it returns IDs.
- Avoid using MCP evidence as equal quality to source evidence unless verified.

## Data Model And OKF Round-Trip Gaps

### 6. Mutable defaults are used across ontology and validation models

Evidence: `ikp_platform/core/validation/validator.py:50-57`

`ValidationResult` list fields use `[]` instead of `Field(default_factory=list)`.

Why it matters: Pydantic v2 protects many common cases, but this is inconsistent, easy to misuse outside model construction, and violates the local standard already used for `evidence`.

How to fix:

- Replace mutable defaults in validation models with `Field(default_factory=list)` or `Field(default_factory=dict)`.
- Add a regression test that two new objects do not share list/dict values.

### 7. OKF reader drops fields that writer persists

Evidence: `ikp_platform/core/repository/okf_writer.py:93-129`, `ikp_platform/core/repository/okf_reader.py:201-245`

Writer dumps most model fields to frontmatter. Reader reconstructs only selected fields for each specialized type. Examples at risk include `inclusive_qty` for components/SKUs, `packaging_type` for components, `variants`, `slot_mapping_ids`, `validated`, `validation_source`, `negated`, `scaling_factor`, and `dependency_targets`.

Why it matters: graph bootstrap after restart can lose semantics that existed at ingestion time. This directly affects quantity limits, package handling, rule interpretation, and topology.

How to fix:

- Create model-specific frontmatter parity tests for every ontology subclass.
- Prefer constructing from frontmatter via Pydantic model validation after parsing relationships/evidence, rather than hand-copying a partial field list.
- For backward compatibility, keep migration defaults for missing old fields.

### 8. OKF writer path computation creates awkward nested rule paths

Evidence: `ikp_platform/core/repository/okf_writer.py:71-80`

Rule IDs already contain platform/rules/rule-NNN. `_compute_path()` also adds platform hierarchy, `rules`, and `platform-rules`, then slugifies the whole ID. Existing generated files collect many rule documents into `rules/platform-rules.md`, while future single writes can create different paths.

Why it matters: path rules are hard to reason about, and approval/update flows can produce duplicate locations.

How to fix:

- Define one canonical path policy per object type.
- For rules, use either one multi-document file per platform or one file per rule, not both.
- Store original file path during read and preserve it during updates.

## Ingestion And Extraction Quality Gaps

### 9. PDF extraction is heavily heuristic and source-specific despite generic names

Evidence: `ikp_platform/core/ingestion/pdf_extractor.py`

The extractor contains HPE-oriented patterns, QuickSpecs assumptions, regexes for specific hardware categories, and hard-coded capability/workload maps.

Why it matters: adding Dell/Cisco/Lenovo PDFs may parse incorrectly while still emitting high-confidence objects.

How to fix:

- Split extraction into vendor/profile adapters: common PDF text/table extraction, then source-family-specific parsers.
- Attach parser name/version to evidence.
- Downgrade confidence when generic heuristics are used outside known profiles.

### 10. Component classification leaves many SKUs as Accessory/General

Evidence: generated repository contains many `component_category: Accessory` / `component_subcategory: General` objects for real orderable items.

Why it matters: solution generation ranks and filters by categories. Poor classification makes components hard to select, validate, and explain.

How to fix:

- Produce a classification review report after ingestion: count `Accessory/General` by source and top repeated descriptions.
- Add synonym maps and table-column aware classification.
- Send low-confidence classifications to review queue.

### 11. Extracted rule text is often truncated or malformed

Evidence: generated `repository/.../rules/platform-rules.md` includes examples such as incomplete sentences and bullet fragments.

Why it matters: malformed rules are hard to interpret deterministically and can become false validation blockers once the rule engine is strengthened.

How to fix:

- Preserve page, line, and surrounding paragraph context.
- Add minimum sentence completeness checks.
- Send fragments to review instead of marking `confidence: High`.
- Add fixture tests for multiline bullets and continuation lines.

### 12. LLM dependency behavior is inconsistent across ingestion and runtime

Evidence: `LLMClient.parse_intent()` and `select_components()` use Gemini SDK; `extract_rules()` and `critic_review_rules()` shell out to `antigravity-cli`.

Why it matters: the same "LLM" capability has different credentials, failure modes, timeouts, logging, and testability.

How to fix:

- Introduce a provider interface for LLM operations.
- Make provider selection explicit in config/status.
- Mock the provider in ingestion tests.
- Remove browser/OAuth-dependent CLI calls from automated ingestion unless explicitly enabled.

## API And Frontend Contract Gaps

### 13. Frontend uses broad `any` types for core API payloads

Evidence: `ikp_web/src/App.tsx`, `SemanticSearch.tsx`, `BoqValidation.tsx`, `SolutionSynthesis.tsx`, `PlatformDashboard.tsx`

Why it matters: API shape drift is easy to miss until runtime. The BOQ UI/API mismatch around `messages` has been fixed, but the broader lack of typed API contracts remains.

How to fix:

- Define TypeScript interfaces for every API response.
- Generate types from Pydantic/OpenAPI or keep a shared schema file.
- Update BOQ UI to render the actual response fields.

### 14. UI error handling is inconsistent and sometimes only console-based

Evidence: `ValidationPortal` uses `alert()`, search failures only log to console, status fetch failure only logs.

Why it matters: users cannot distinguish empty results from failed API calls or missing vector index.

How to fix:

- Add visible error states for every API call.
- Show integration/index health from `/api/status`.
- Replace `alert()` with in-app error UI.

### 15. E2E tests are smoke tests, not behavior tests

Evidence: `ikp_web/tests/e2e/search.spec.ts`, `validation.spec.ts`

Current tests mostly assert the app renders. They do not mock API responses, navigate to each tab, or assert search/BOQ/review behavior.

Why it matters: the frontend can build or render while core workflows are broken.

How to fix:

- Use Playwright route mocks for `/api/status`, `/api/search`, `/api/boq/validate`, and `/api/review-queue`.
- Assert each tab renders expected states and handles failure responses.
- Run E2E tests as a behavior gate after route mocks are in place.

## Quality Gates And Tooling Gaps

### 16. Backend tests pass but miss important production branches

Evidence: tests mock workflow generator, use heuristic LLM fallback, and do not cover real dynamic validation, alias learning across restart, deterministic trigger evaluation, or review path preservation.

Why it matters: passing tests currently mean "known historical regressions are guarded," not "solution quality is correct."

How to fix:

- Add targeted tests for every critical gap in this audit.
- Keep tests hermetic, as current fixtures correctly avoid real `repository/` writes.

## Documentation Drift And Ambiguities

### 17. Documentation generation can still drift from runtime checks

Evidence: `CONTEXT.md`, `STATE.md`, and generated graph reports can be updated by scripts or agents independently of code-level capability checks.

Why it matters: docs have been manually synchronized, but future changes can reintroduce stale claims unless docs are regenerated from actual runtime status where possible.

How to fix:

- Add a lightweight docs/status check that compares documented ports, capability flags, and placeholder warnings against code/config.
- Generate `CONTEXT.md` from persisted source registry and explicit capability probes where possible.
- Keep `IKP/standards/11_CURRENT_IMPLEMENTATION_STACK.md` as the canonical manual override when automated generation is incomplete.

## Recommended Implementation Plan

### Phase 1: Fix Reasoning Correctness

- Replace severity-only rule failure with deterministic trigger/condition evaluation.
- Add tests for satisfied and violated require/incompatibility rules.
- Add regression tests for bounded workflow termination and ambiguous BOQ platform behavior already implemented.

### Phase 2: Make Learning Real

- Persist delta statuses and review decisions.
- Add restart tests for alias support and BOQ correction persistence.
- Preserve original OKF file paths for review approvals.
- Connect API/CLI review flows to `LearningEngine`.

### Phase 3: Improve Ingestion Fidelity

- Add OKF field parity tests and reader fixes.
- Add ingestion quality reports for `Accessory/General`, malformed rules, and low-confidence objects.
- Split source-family parsers and confidence policies.

### Phase 4: Strengthen UI/API Contracts

- Define TypeScript interfaces or generated OpenAPI types for every endpoint.
- Add visible error states for every API call.
- Convert E2E smoke tests into behavior tests with route mocks.

### Phase 5: Keep Docs Honest

- Add a docs/status consistency check for ports, placeholder integrations, and generated state lifecycle.
- Keep `README.md`, `SETUP.md`, `CONTEXT.md`, KT, and Standard 11 synchronized when endpoint payloads or workflow behavior changes.

## Reaudit Checklist

Use this checklist after fixes:

- `uv run pytest -q` passes.
- `npm run build` passes.
- `npm run lint` has zero warnings or documented accepted warnings.
- `uv run ruff check .` passes or has a deliberate scoped config.
- `make lint` works from a fresh `uv sync --extra dev`.
- Rule tests prove satisfied rules do not fail.
- Workflow invalid requests terminate cleanly.
- Review approval updates the original OKF file path.
- Alias learning persists across restart.
- `CONTEXT.md` does not claim placeholder integrations are complete.
