---
name: epistemic-gap-mapper-skill
description: Map frame-challenging hypotheses against target papers and target narratives without judging truth. Use when Codex needs to analyze a manuscript, outsider or interdisciplinary hypothesis, breakthrough claim, controversial argument, or research proposal by extracting claims, separating paper conflict from narrative conflict, auditing A/B/C/X/M tier declarations, identifying overclaims, gaps, exceptions, falsifiers, narrative debt, safer wording, node graphs, narrative audits, target-paper diffs, local claim-evidence checks, or Breakthrough Diagnosis reports.
---

# Epistemic Gap Mapper

Use this skill to make a bold or frame-challenging hypothesis legible to expert review. Map the argument structure; do not decide whether the hypothesis is true.

## Core Rules

- Separate `Target Paper` from `Target Narrative`.
- Treat target papers as specific sources with explicit claims, data, authors, and limits.
- Treat target narratives as diffuse standard stories from reviews, textbooks, disciplinary habit, synthesis, or AI-frequency summaries.
- Do not collapse a diffuse narrative into a paper unless the paper explicitly makes that claim.
- Do not reject a claim merely because it challenges consensus.
- Do mark claims as overclaims when they exceed their support.
- Do not invent citations. Mark uncertain sources as verification needed.
- Treat comparisons and analogies as `heuristic_analogy_for`, not direct evidence.
- Produce structured audit material rather than a numeric score or global truth verdict.
- Let humans declare final A/B/C/X/M tiers. LLMs may propose candidates and audit consistency, but they must not be treated as final arbiters.

## Reference Map

Load only the files needed for the current task:

- `docs/workflow.md`: read for the complete staged workflow.
- `docs/node_schema.md` and `docs/edge_schema.md`: read when designing or explaining graph structure.
- `docs/narrative_audit.md`: read when separating target papers from target narratives.
- `docs/methodological_index.md`: read when tagging reasoning methods or analogies.
- `docs/tool_falsifiability.md`: read when checking whether the mapper itself is failing as a method.
- `schemas/node_schema.json`, `schemas/edge_schema.json`, `schemas/graph_schema.json`, and `schemas/report_schema.json`: read before producing machine-checkable JSON.
- `prompts/*.md`: use when the user wants reusable copy-paste prompts.
- `templates/*.md`: use when starting an intake, target-paper table, target-narrative table, or diagnosis report.
- `templates/first_map_template.md`, `templates/nodes_template.json`, and `templates/graph_template.md`: use when the user needs the fastest possible first map.
- `examples/starter_cafe_rain/`: use as the low-friction first example before the larger research case.
- `examples/jomon_dotaku_kiki/nodes_minimal.json`: use as the compact worked graph for learning the node system.
- `examples/jomon_dotaku_kiki/nodes_full.json`: use as the fuller worked graph when the user needs broad coverage of the Jomon / Dotaku / Kiki case.
- `examples/jomon_dotaku_kiki/graph_sample_grouped.md`: use when the full graph needs a readable grouped Mermaid view.
- `examples/jomon_dotaku_kiki/prose_case/`: read when the user needs a prose-only case study or wants to decompose prose into nodes.
- `outreach/public_explainer_jp.md` and `outreach/public_explainer_en.md`: use when the user needs a public-facing explanation of the project.
- `outreach/recruitment_posts.md`: use when the user needs collaborator recruitment, community invitation, or launch post language.

## Workflow

1. Intake the hypothesis, manuscript, known target papers, suspected target narratives, and intended use. If the user has not provided structure, use `templates/hypothesis_intake.md`.
2. Extract the central hypothesis, main claims, evidence claims, inference claims, speculative claims, assumptions, and dangerous overclaims.
3. Identify target papers. For each paper, state what it supports, what it does not support, and how the hypothesis accepts, extends, challenges, or reframes it.
4. Identify target narratives. For each narrative, list component claims, source status, evidence trace, citation debt, and the hypothesis relationship.
5. Build a node and edge graph using `node_id`, `node_type`, `text`, `tier`, `domain`, `confidence`, relation fields, and relevant metadata.
6. Run Stage 5A structural audit: citation coverage, analogy marking, falsifier presence, definition consistency, paper/narrative separation, and overclaim phrases.
7. Run Stage 5B human tier declaration: the author, expert, reviewer, or operator declares final A/B/C/X/M tiers with `declared_tier`, `tier_declared_by`, `tier_rationale`, and `tier_review_status`. LLM output can propose candidates only.
8. Run Stage 5C local claim-evidence checks: for each declared claim-evidence pair, record whether the cited source locally supports, hedges, presupposes, contradicts, contextualizes, or only analogizes the claim.
9. Run Stage 5D graph handoff: provide the graph and local audit findings for human global review without asking the LLM for a truth verdict.
10. Compare each target paper with the hypothesis and distinguish direct contradiction, scope gap, frame conflict, overextension, methodological mismatch, and no conflict.
11. Audit each target narrative and separate paper-supported claims from disciplinary habit or untraced narrative.
12. Produce a Breakthrough Diagnosis with status, A-level foundations, B-level contributions, C-level vulnerabilities, X-level problems, required patches, falsification plan, and recommended next action.

## A/B/C/X/M Tiers

Tiers are declarations, not LLM judgments. The LLM may suggest candidate tiers, but final graph data should mark who declared the tier and whether review is complete.

- `A`: relatively strong claim supported by existing data or scholarship.
- `B`: plausible hypothesis consistent with current evidence but not proven.
- `C`: not yet assertable, but testable or worth preserving as a research question.
- `X`: unsupported, overclaimed, internally inconsistent, or contradicted by evidence.
- `M`: methodological tag or heuristic analogy, not direct evidence.

Preserve C-level claims when they are clearly labeled and testable. Any C-tier `UserClaimNode` must link to at least one `FalsifierNode`. Patch X-level claims with safer wording or remove them from the asserted argument.

## Graph Rules

- Use `PaperNode` for specific papers, books, reports, datasets, preprints, excavation reports, or primary texts.
- Use `SourceClaimNode` for claims actually made by target papers.
- Use `UserClaimNode` for claims made by the user's manuscript.
- Use `NarrativeNode` for standard stories or diffuse frames.
- Use `NarrativeTraceNode` for candidate sources that clarify whether a narrative is directly supported, partially supported, merely compatible, or still carrying citation debt.
- Use `RiskNode` for overclaim risks.
- Use `FalsifierNode` for evidence that would weaken or falsify a claim.
- Use `MethodNode` for methodological tags and analogies.
- Use `supports_weakly` for plausible but non-decisive support.
- Use `challenges_narrative` only when the target is a `NarrativeNode`.
- Use `heuristic_analogy_for` for comparisons, historical parallels, mythological parallels, or method analogies.
- Do not use `supports` from a `MethodNode`.
- Use edge metadata such as `support_strength`, `support_mode`, `local_check_status`, `claim_scope_match`, `vocabulary_match`, and `granularity_match` when inspecting local claim-evidence support.

## Output Style

Be clear, rigorous, and non-grandiose. Prefer node-specific criticism over broad dismissal. When a claim is weak, explain what evidence is missing and what wording would make it safer. Always keep expert review and human calibration visible in the output.

## CLI Helpers

Use the lightweight CLI only for local graph checks:

```bash
python scripts/egm_cli.py validate examples/starter_cafe_rain/nodes_starter.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_minimal.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_full.json
python scripts/egm_cli.py render examples/jomon_dotaku_kiki/nodes_full.json --mermaid
```

When packaging or testing this skill, validate the skill folder with the skill-creator `quick_validate.py` script.
