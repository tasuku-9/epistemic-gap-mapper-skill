# Quickstart

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

## Step 6 — Diagnose A/B/C/X/M

Use `prompts/05_abcx_diagnosis.md`.

## Step 7 — Compare with target papers

Use `prompts/06_target_paper_diff.md`.

## Step 8 — Audit narratives

Use `prompts/07_narrative_audit.md`.

## Step 9 — Produce breakthrough diagnosis

Use `prompts/08_breakthrough_diagnosis.md`.

## Optional — Validate or render a node graph

```bash
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_minimal.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_full.json
python scripts/egm_cli.py render examples/jomon_dotaku_kiki/nodes_full.json --mermaid
```

## Principle

Do not ask the AI to judge the hypothesis first. Ask it to map the structure first.
