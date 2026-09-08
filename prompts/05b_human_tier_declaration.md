# Prompt 05B - Human Tier Declaration

```text
Use this step after the structural audit.

The final A/B/C/X/M tier must be declared by a human author, domain expert, reviewer, or project operator.
The LLM may summarize evidence and propose candidates, but it must not be treated as the final tier authority.

If no explicit human decision is available, output proposed_tier and tier_review_status: proposed (or needs_review), with a candidate rationale. Omit declared_tier, tier_declared_by, and tier_declaration_ref. Never invent an approval, infer it from silence, or use a template's default as a decision.

For each UserClaimNode, fill:

- node_id
- declared_tier: A / B / C / X / M
- tier_declared_by: name or stable pseudonymous identifier of the actual human, not a role alone
- tier_declaration_ref: retrievable message or review-log locator for the explicit decision
- tier_rationale
- tier_review_status: declared / reviewer_checked / disputed for a recorded declaration
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
- Propose X when a claim exceeds its sources or contradicts inspected evidence; the human declares the final tier. Missing source access alone is needs_source, not proof of falsehood.
- If a claim is X, declare how it fails with one or more failure_modes: evidence_laundering, analogy_inflation, narrative_capture, falsifier_removal, citation_debt, scope_jump.
- C is allowed only when the claim is explicit, testable, and linked to at least one FalsifierNode.
- Method or analogy nodes are M, not evidence.

Only when a human decision is actually recorded, output graph patch fields for that UserClaimNode:

{
  "declared_tier": "...",
  "tier_declared_by": "...",
  "tier_declaration_ref": "...",
  "tier_rationale": "...",
  "tier_review_status": "...",
  "failure_modes": ["..."]
}
```
