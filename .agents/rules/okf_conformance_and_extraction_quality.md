---
description: "OKF spec conformance and extraction-quality bar — findings from the 2026-07-18 phase-2 audit"
---

# OKF Conformance & Extraction Quality

These are open findings from `IKP/audit_phase2/PHASE2_AUDIT_AND_SYNC_PLAN.md`
(2026-07-18). They are not yet resolved — this file exists so agents doing
further ingestion/repository work don't accidentally make them worse before
they're deliberately addressed, and know where to look for the full context.

## 1. Rule files are not currently one-concept-per-file (OKF §2, §4)

`OKFWriter` groups multiple `Rule` concepts into a single physical `.md`
file per platform/category (e.g. `cpu-rules.md` can contain dozens of
separate `---frontmatter---` blocks, one per rule). `OKFReader` has a custom
multi-block scanner to read them back apart. This works fine for this
codebase's own reader/writer, but it means `repository/` is **not**
conformant with the external OKF spec (`IKP/references/OKF_SPECIFICATION.md`
§2, §4), which defines a Concept as one file with one frontmatter block. A
generic OKF consumer pointed at this repository would silently only see the
first rule in each grouped file.

**Do not extend this pattern to other object types** (e.g. don't start
grouping multiple `Component` or `SKU` concepts into one file "for
consistency") until this is resolved one way or the other — see the audit
doc for the two options under consideration (make grouped files spec-
conformant via a nested `rules/<category>/<rule-id>.md` layout, vs.
documenting it as an intentional non-conformant extension via a new ADR).

## 2. Extracted Rule titles must carry real semantic identity

Every rule extracted so far is titled `Engineering Rule 1`, `Engineering
Rule 2`, etc. (a sequence number, not a description). Blueprint 03 §8
requires every rule to expose a meaningful "Identity." ADR-001 fixed the
*file-collision* consequence of generic titles (filenames no longer depend
on title), but the underlying extraction gap is still open: nothing derives
a real title from the rule's own text.

**Rule:** If you're touching `pdf_extractor.py`'s rule-extraction path,
derive the title from `expected_outcome` or the first several words of the
rule body — do not add more generic sequential titles. If you can't derive a
meaningful title without more context than is locally available, that's a
sign the extraction pass needs to look at more surrounding text before
constructing the `Rule` object, not a sign to fall back to `Engineering Rule
N`.

## 3. Don't add a new ontology object type without a real extraction path

`Constraint` (generic, non-`CategoryLimit`), `Variant`, `SolutionCategory`,
and `Configuration` are fully modeled in `models.py` with complete OKF
reader/writer support, but as of the 2026-07-18 audit, **no ingestion or
reasoning code anywhere constructs an instance of any of them.** They're
dead code paths that exist only in the schema.

**Rule:** If you add a new `EngineeringObjectType` / model subclass, either
(a) also add at least one real call site that constructs it during
ingestion/reasoning in the same change, or (b) explicitly note it as
"modeled, not yet extracted" in `IKP/standards/10_IMPLEMENTATION_CHECKLIST.md`
so it's tracked rather than silently unused. The Excel parser and Portal
parser (both still "Pending" on the checklist) are the most natural places
`Variant` and `Configuration` extraction would actually get built out.

## 4. New Pydantic fields reach the graph automatically — see graph_serialization.md

Separate but related: if your extraction work adds new fields to any
ontology model, see `.agents/rules/graph_serialization.md` for how
`GraphBuilder.add_concept` handles that now (automatically, via
`model_dump`) and what to do if you're adding an Excel/Portal parser that
needs a new object type covered by `tests/test_graph_field_parity.py`.
