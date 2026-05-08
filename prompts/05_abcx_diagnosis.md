# Prompt 05 - Calibration Audit Workflow

```text
Use this as the navigation prompt for Stage 5.

Do not ask the LLM to decide whether the hypothesis is true.
Do not ask the LLM to issue the final A/B/C/X/M tier.

Run Stage 5 in four passes:

1. 05A Structural Audit
   Use prompts/05a_structural_audit.md.
   The LLM checks graph structure, citation coverage, analogy marking, falsifier presence, definition consistency, paper/narrative separation, overclaim phrases, and X-tier failure modes.

2. 05B Human Tier Declaration
   Use prompts/05b_human_tier_declaration.md.
   The human author, expert, reviewer, or operator declares final A/B/C/X/M tiers. The LLM may propose candidate tiers only.

3. 05C Local Claim-Evidence Check
   Use prompts/05c_local_fact_check.md.
   For each declared claim-evidence pair, check local support only: direct, hedged, presupposed, contextual, counter-example, analogy-only, no direct support, or unknown.

4. 05D Graph Handoff
   Use prompts/05d_graph_handoff.md.
   Hand off graph data and local audit findings for human global review. Do not provide a global truth verdict.

Core rule: calibration is an audit surface, not an AI judgment surface.
```
