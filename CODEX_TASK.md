# Codex Task

You are improving **Epistemic Gap Mapper Skill**, a prompt-and-schema based skill for mapping frame-challenging hypotheses against target papers and target narratives.

## Priorities

1. Preserve the core philosophy: no truth scoring, no automatic rejection for challenging consensus, and no collapse of target papers into target narratives.
2. Keep `SKILL.md` concise and procedural. Move detailed examples, schemas, and reusable text into `docs/`, `schemas/`, `prompts/`, `templates/`, `examples/`, or `outreach/`.
3. Strengthen validation without turning the project into a heavy software package.
4. Keep worked examples explicit about uncertainty, overclaim risks, and falsification conditions.
5. Keep the first-use path simple enough for a new user to complete before reading the advanced examples.
6. Improve public-facing explanation without making the project sound like a manifesto or a fringe-theory amplifier.
7. Keep calibration audit-oriented: LLMs can propose candidate tiers and local checks, but humans declare final A/B/C/X/M tiers.

## Guardrails

- Do not add a numeric scoring system.
- Do not implement automatic truth judgment.
- Do not ask the LLM for a global truth verdict or global consistency verdict.
- Do not invent citations or make the tool appear to verify sources automatically.
- Do not treat comparisons, myths, analogies, or historical parallels as direct evidence.
- Do not classify speculative claims as A-level claims.
- Do not let C-level UserClaimNodes stand without at least one falsifier link.
- Do not treat "no source found" as proof that a target narrative is false.
- Do not remove the distinction between `PaperNode`, `SourceClaimNode`, and `NarrativeNode`.

## Useful Next Improvements

1. Add or refine type-specific validation for `schemas/node_schema.json`.
2. Keep `schemas/graph_schema.json` aligned with `node_schema.json` and `edge_schema.json`.
3. Extend `scripts/egm_cli.py` semantic checks when a project rule can be validated deterministically.
4. Expand worked examples so every major node type appears at least once.
5. Add tests or GitHub Actions only if they remain lightweight and dependency-minimal.
6. Add more examples from domains outside the Jomon / Dotaku / Kiki case.
7. Preserve the starter example and templates as a low-friction first step.
8. Use `docs/tool_falsifiability.md` when evaluating whether the mapper itself is becoming too judge-like or too permissive.

## Validation

Before committing changes, run:

```bash
python scripts/egm_cli.py validate examples/starter_cafe_rain/nodes_starter.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_minimal.json
python scripts/egm_cli.py validate examples/jomon_dotaku_kiki/nodes_full.json
python scripts/egm_cli.py render examples/jomon_dotaku_kiki/nodes_full.json --mermaid
```

If Codex skill-creator tools are available, also run `quick_validate.py .`.
