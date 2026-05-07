# Prompt 05 — A/B/C/X Diagnosis

```text
Using the node graph, diagnose each UserClaimNode with A/B/C/X/M tiers.

Definitions:
A = relatively strong claim supported by existing data or scholarship.
B = plausible hypothesis consistent with current evidence but not proven.
C = not yet assertable but testable or worth preserving as a research question.
X = unsupported, overclaimed, internally inconsistent, or contradicted by evidence.
M = methodological tag or heuristic analogy, not direct evidence.

For each UserClaimNode, output:

- Proposed Tier
- Reason for Tier
- Supporting Evidence
- Missing Evidence
- Overclaim Risk
- Safer Wording
- What would falsify or weaken it?
- Human Review Needed: yes / no

Rules:
- Do not classify a claim as X merely because it challenges consensus.
- Do classify a claim as X if it overstates the evidence.
- C is not failure. C is a testable frontier.
```
