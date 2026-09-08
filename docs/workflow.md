# Workflow

Epistemic Gap Mapper follows a staged workflow. The order matters: do not ask the AI to evaluate the hypothesis before it has extracted the structure.

## Stage 1 - Manuscript claim extraction

Goal: extract the user's central hypothesis, claims, evidence, assumptions, and possible overclaims.

Output:

- Central Hypothesis
- Main Claims
- Evidence Claims
- Inference Claims
- Speculative Claims
- Dangerous Overclaims

## Stage 2 - Target paper discovery

Goal: identify the papers and primary sources the manuscript is actually in conversation with.

Target papers are classified as:

- Canonical Frame Papers
- Data-Anomaly Papers
- Bridge Papers
- Adversarial Papers
- Primary Sources

## Stage 3 - Target narrative extraction

Goal: identify the diffuse standard narrative the hypothesis challenges.

A target narrative may be:

- primary-supported,
- review-supported,
- textbook-canonical,
- synthetic consensus,
- disciplinary habit,
- AI-frequency narrative,
- or untraced narrative.

## Stage 4 - Node construction

Goal: convert papers, claims, evidence, narratives, gaps, exceptions, risks, and falsifiers into nodes.

Do not evaluate yet. Build the map first.

## Stage 5 - Calibration audit

Goal: make claim status auditable without asking the LLM for a global verdict.

### Stage 5A - LLM Structural Audit

The LLM checks the graph structure, not the truth of the hypothesis.

Audit fields:

- citation coverage,
- analogy marking,
- falsifier presence,
- definition consistency,
- paper/narrative separation,
- overclaim phrases,
- X-tier failure modes.

Output:

- missing or weak citation links,
- unmarked analogies,
- C-tier candidates lacking falsifiers,
- terms that need definition or scope control,
- places where target papers and target narratives blur,
- phrases that exceed local source support,
- X-tier nodes missing `failure_modes`.

### Stage 5B - Human Tier Declaration

The human author, domain expert, reviewer, or project operator declares final A/B/C/X/M tiers.

The LLM may propose tier candidates, but final graph data must keep human declaration visible with:

- `declared_tier`,
- `tier_declared_by`,
- `tier_declaration_ref`,
- `tier_rationale`,
- `tier_review_status`.

Before an explicit human decision, use `proposed_tier` and a provisional status; omit declaration fields. See [Audit Records](audit_records.md). Do not fabricate a named reviewer or approval event to finish this stage. Local checks and a pending-review handoff can proceed without a final tier.

Tier meanings:

- A = relatively strong.
- B = plausible hypothesis.
- C = not yet assertable, but testable.
- X = overclaimed or unsupported.
- M = methodological or heuristic.

Any C-tier `UserClaimNode` must have at least one linked `FalsifierNode`.

Any X-tier node must declare at least one `failure_modes` value so reviewers can see how the claim breaks.

### Stage 5C - LLM Local Claim-Evidence Check

For each declared claim-evidence pair, the LLM checks only whether the cited source locally supports the claim.

Local support options:

- directly supports,
- hedges,
- presupposes,
- contradicts,
- contextualizes,
- supplies analogy only,
- provides no direct support,
- unknown / needs source.

This stage records edge-level metadata such as `support_strength`, `support_mode`, `source_span`, `local_check_status`, `claim_scope_match`, `vocabulary_match`, and `granularity_match`.

Inspect the actual source, then record `source_ref`, a short `source_excerpt`, `checked_by`, and `local_check_notes`. If access or verification is missing, use `needs_source` and unknown support. Neither schema validation nor a `supports` edge proves that a source was checked.

### Stage 5D - Human Global Review

Do not ask the LLM for a global truth verdict or global consistency verdict.

The LLM hands off:

- the graph,
- structural audit findings,
- declared tier metadata,
- local claim-evidence checks,
- unresolved citation debt,
- falsification and patch requirements.

The human reviewer decides what the map means.

## Stage 6 - Target paper diff

Goal: determine whether the manuscript conflicts with a source, extends it, or simply uses it as an evidentiary foundation.

Conflict types:

- direct contradiction,
- scope gap,
- frame conflict,
- overextension,
- methodological mismatch.

## Stage 7 - Narrative audit

Goal: determine whether the manuscript is challenging actual papers or a diffuse standard narrative.

Narrative audit includes:

- component claims,
- source trace,
- citation debt,
- accepted elements,
- challenged elements,
- reframed elements.

## Stage 8 - Breakthrough diagnosis

Goal: produce a structured diagnosis, not a score or truth verdict.

Report audit readiness and unresolved decisions, not an LLM prediction that a breakthrough is possible. Keep candidate tiers explicitly provisional and attach human declaration references only when they exist.

Output:

- Breakthrough Status
- A-level Foundations
- B-level Contributions
- C-level Vulnerabilities
- X-level Problems
- Required Patches
- Falsification Plan
- Recommended Next Action
