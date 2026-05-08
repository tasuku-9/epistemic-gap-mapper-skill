# Prompt 05B - Human Tier Declaration

```text
Use this step after the structural audit.

The final A/B/C/X/M tier must be declared by a human author, domain expert, reviewer, or project operator.
The LLM may summarize evidence and propose candidates, but it must not be treated as the final tier authority.

For each UserClaimNode, fill:

- node_id
- declared_tier: A / B / C / X / M
- tier_declared_by: author / expert / reviewer / operator / other named human role
- tier_rationale
- tier_review_status: proposed / declared / reviewer_checked / needs_review / disputed / unknown
- falsifier_link_required: yes / no
- linked_falsifiers
- failure_modes, required if declared_tier is X

Tier guide:

- A = relatively strong claim supported by existing data or scholarship.
- B = plausible hypothesis consistent with current evidence but not proven.
- C = not yet assertable, but testable or worth preserving as a research question.
- X = unsupported, overclaimed, internally inconsistent, or contradicted by evidence.
- M = methodological tag or heuristic analogy, not direct evidence.

Rules:

- Do not mark a claim X merely because it challenges consensus.
- Do mark a claim X when it exceeds its sources, contradicts cited evidence, or cannot be repaired with narrower wording.
- If a claim is X, declare how it fails with one or more failure_modes: evidence_laundering, analogy_inflation, narrative_capture, falsifier_removal, citation_debt, scope_jump.
- C is allowed only when the claim is explicit, testable, and linked to at least one FalsifierNode.
- Method or analogy nodes are M, not evidence.

Output graph patch fields for each UserClaimNode:

{
  "declared_tier": "...",
  "tier_declared_by": "...",
  "tier_rationale": "...",
  "tier_review_status": "...",
  "failure_modes": ["..."]
}
```
