# Prompt 05A - LLM Structural Audit

```text
Using the current node graph, run a structural audit.

Do not decide whether the hypothesis is true.
Do not assign final A/B/C/X/M tiers.
You may propose tier candidates only when useful, and they must be marked as non-final.

Check:

- Citation coverage:
  Which UserClaimNodes lack local source support?
  Which source links are weak, missing, unverifiable, or too broad?

- Analogy marking:
  Are comparisons, historical parallels, myths, or methods marked as heuristic_analogy_for or not_direct_evidence?
  Flag any analogy being treated as evidence.

- Falsifier presence:
  Does every C-tier candidate have at least one FalsifierNode?
  Which B-tier or broad synthesis claims would benefit from falsifiers?

- Definition consistency:
  Which terms need vocabulary_map, definition_scope, or granularity_justification?
  Are key terms used at different scales in different nodes?

- Paper/narrative separation:
  Are Target Papers, SourceClaimNodes, NarrativeNodes, and NarrativeTraceNodes distinct?
  Flag any diffuse narrative being collapsed into a paper.

- Overclaim phrases:
  Identify phrases that exceed the cited source.
  Suggest safer wording without erasing testable C-level claims.

- X-tier failure modes:
  For each X-tier candidate, identify how the claim breaks.
  Use failure_modes: evidence_laundering, analogy_inflation, narrative_capture, falsifier_removal, citation_debt, scope_jump.

Output:

1. Structural Audit Table
   - node_id
   - issue_type
   - finding
   - severity: pass / warn / fail / needs_source
   - failure_modes, if X-tier or X-tier candidate
   - suggested_patch

2. Candidate Tier Notes
   - node_id
   - candidate_tier
   - why this is only a candidate
   - human declaration needed: yes

3. Required Graph Metadata
   - missing node metadata
   - missing edge metadata
   - missing falsifiers
```
