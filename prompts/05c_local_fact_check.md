# Prompt 05C - LLM Local Claim-Evidence Check

```text
For each declared claim-evidence pair, check local source support only.

Do not decide whether the whole hypothesis is true.
Do not issue a global consistency verdict.
Do not upgrade or downgrade final tiers unless a human reviewer asks you to prepare candidate notes.

For each edge or cited support relation, inspect whether the source locally:

- directly supports the claim,
- hedges the claim,
- presupposes the claim,
- contextualizes the claim,
- supplies a counter-example,
- supplies analogy only,
- provides no direct support,
- remains unknown or needs source verification.

Record edge metadata:

- support_strength: direct / hedged / presupposed / contextual / counter_example / analogy_only / no_direct_support / unknown
- support_mode: empirical / textual / inferential / methodological / comparative / narrative_trace
- source_span: exact page, passage, figure, table, node, or "not specified"
- local_check_status: pass / warn / fail / needs_source
- claim_scope_match: full / partial / mismatch / unknown
- vocabulary_match: same_terms / mapped_terms / ambiguous / mismatch
- granularity_match: same_grain / too_broad / too_narrow / atomized / unknown

Output:

1. Local Claim-Evidence Table
   - edge or relation id
   - claim node
   - source node
   - local support finding
   - metadata patch

2. Repair Notes
   - wording to narrow
   - source span needed
   - claim split needed
   - source replacement needed

3. Non-Evidence Warnings
   - any MethodNode, analogy, comparison, or NarrativeTraceNode being treated as direct evidence
```
