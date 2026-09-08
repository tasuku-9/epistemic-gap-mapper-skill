# Audit Records

Validation checks record structure, not scientific truth, source authenticity, or a person's identity. Never manufacture a completed check or human approval to satisfy the validator.

## Tier proposals and declarations

- Use `proposed_tier` for an LLM candidate and `tier_review_status: proposed` or `needs_review`. `tier` remains a backwards-compatible display field; without `declared_tier`, it is provisional, not a final decision.
- Set `declared_tier` only after an explicit human decision. Record a named or stable pseudonymous human in `tier_declared_by`, the reason in `tier_rationale`, and a retrievable message or review-log locator in `tier_declaration_ref`. A role such as `author` alone is insufficient.
- A declaration has status `declared`, `reviewer_checked`, or `disputed`. Keep `tier` consistent with it. A different LLM suggestion can remain in `proposed_tier`; it does not overwrite the human decision.
- Without an actual approval record, omit the declaration fields. Do not fill them with example names, inferred consent, or placeholders. The CLI can reject incomplete records but cannot authenticate a human decision.

## Local source inspections

`needs_source` means the source has not been inspected sufficiently. Omitted local-check metadata is also pending. Do not infer `pass`, `direct`, or `full` from a `supports` relation, a citation title, or a plausible narrative.

A completed `pass`, `warn`, or `fail` requires:

- `source_ref`: a `PaperNode` identifying the particular document inspected;
- that source's `verification_status: verified`, meaning the document was available and its identity checked, not that all its claims are true;
- `source_span`: a precise page, paragraph, table, figure, or local file and line;
- `source_excerpt`: a short faithful excerpt, within applicable quotation limits;
- `checked_by`: the actual human or explicitly identified LLM checker;
- `local_check_notes`: the local finding and its limitations;
- `support_strength`: the finding, not `unknown`.

`pass` means the recorded local relation survived the inspection. `warn` records partial, hedged, or contextual support. `fail` records a local mismatch or lack of support, not a global verdict. A failed check does not automatically declare a tier X. An excerpt and metadata remain reviewable assertions: the CLI does not retrieve a paper or prove the excerpt faithful.

For uninspected evidentiary links, use `needs_source`, `support_strength: unknown`, and unknown scope/granularity. Structural analogy marking may use `analogy_only` without asserting a completed source check. Future falsifiers are conditions, not already observed counter-evidence.

## Open questions are valid data

Empty `supporting_sources`, `risks`, or narrative lists are allowed. Missing support is surfaced as citation debt, not as falsehood. Every supplied reference must resolve to an appropriate node; multi-source `source` values are arrays of IDs, not strings such as `E1 + E2`.

Any C-tier UserClaimNode, including a C candidate, requires a FalsifierNode through its `falsifiers` list or a `claim -> falsified_by -> FalsifierNode` edge. Add `test_plan` with a measurement, weakening result, and alternative explanation; a missing plan remains a visible warning. Merely attaching a falsifier does not override already observed contradictory evidence.

## Rendering and migration

The graph is the source of truth for generated diagrams. `render --grouped` uses `metadata.cluster` and requests Mermaid's ELK renderer for cross-cluster links. Use an ELK-capable Mermaid viewer; the ungrouped output remains available for other viewers. Labels distinguish candidate and declared tiers, and pending local checks remain visible. Dotted links can mean unchecked support or non-evidentiary structure; read the relation label. Solid support links indicate a recorded local pass, not global truth.

Older examples used Falsifier-to-claim `falsified_by` edges and Assumption-to-inference `depends_on` edges. Reverse these to match the predicates: claim depends on assumption; claim would be weakened by falsifier. Invalid graphs must be repaired before rendering; the old `--force` bypass is no longer supported.

The existing research and cafe examples are illustrative and unverified, not completed audits. The small `examples/calibration_local_support/` case supplies its fictional source text, so its local textual checks can be inspected without implying real-world evidence or human tier approval.
