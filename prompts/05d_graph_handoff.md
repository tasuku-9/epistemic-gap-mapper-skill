# Prompt 05D - Graph Handoff for Human Global Review

```text
Prepare the graph and audit findings for human global review.

Do not provide:

- a global truth verdict,
- a global consistency verdict,
- a numeric score,
- automatic rejection for challenging consensus.

Provide:

1. Graph Summary
   - main UserClaimNodes
   - Target Paper links
   - Target Narrative links
   - NarrativeTraceNodes and citation debt
   - MethodNodes and analogies
   - RiskNodes and FalsifierNodes

2. Human Tier Declaration Summary
   - declared_tier
   - tier_declared_by
   - tier_review_status
   - unresolved declarations

3. Local Claim-Evidence Findings
   - pass
   - warn
   - fail
   - needs_source

4. Required Human Decisions
   - claims needing reviewer judgment
   - sources needing verification
   - C-tier claims lacking adequate falsification design
   - X-risk phrases needing repair or removal

5. Machine-Readable Patch Suggestions
   - node metadata additions
   - edge metadata additions
   - missing falsifier nodes
   - safer wording patches

Final sentence:
This is an audit handoff for human review, not a truth judgment.
```
