# Quickstart

## First 10 minutes

If you are new to Epistemic Gap Mapper, start with the small example:

- `examples/starter_cafe_rain/README.md`
- `examples/starter_cafe_rain/nodes_starter.json`
- `templates/first_map_template.md`

The goal is to fill a small map before writing a long argument.

## Step 1 — Start with guardrails

Open `prompts/00_system_guardrails.md` and paste it into your AI session.

## Step 2 — Extract your claims

Use `prompts/01_extract_claims.md` with your manuscript.

## Step 3 — Ask for target papers

Use `prompts/02_find_target_papers.md`.

## Step 4 — Ask for target narratives

Use `prompts/03_extract_target_narratives.md`.

## Step 5 — Build nodes

Use `prompts/04_build_nodes.md`.

## Step 6 — Run the calibration audit

Use the Stage 5 prompt set:

- `prompts/05_abcx_diagnosis.md` for the overview.
- `prompts/05a_structural_audit.md` for LLM structural audit.
- `prompts/05b_human_tier_declaration.md` for human-declared A/B/C/X/M tiers.
- `prompts/05c_local_fact_check.md` for local claim-evidence checks.
- `prompts/05d_graph_handoff.md` for human review handoff.

## Step 7 — Compare with target papers

Use `prompts/06_target_paper_diff.md`.

## Step 8 — Audit narratives

Use `prompts/07_narrative_audit.md`.

## Step 9 — Produce breakthrough diagnosis

Use `prompts/08_breakthrough_diagnosis.md`.

## Optional — Validate or render a node graph

```bash
python scripts/egm_cli.py validate examples/starter_cafe_rain/nodes_starter.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_minimal.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_sample.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_full.json
python scripts/egm_cli.py validate templates/nodes_template.json
python scripts/egm_cli.py render examples/jomon_dotaku_kiki/nodes_full.json --mermaid
```

## Principle

Do not ask the AI to judge the hypothesis first. Ask it to map the structure first, then audit local support for human review.
