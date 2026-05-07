# Epistemic Gap Mapper Skill

**Epistemic Gap Mapper** is a prompt-and-schema based skill for analyzing *frame-challenging hypotheses*.

It does **not** decide whether a hypothesis is true. Instead, it maps how a new hypothesis relates to:

- target papers,
- target narratives,
- evidence,
- assumptions,
- gaps,
- exceptions,
- overclaims,
- and falsification conditions.

The goal is to turn a fragile or outsider hypothesis into a structure that specialists can actually inspect.

> It does not replace expertise. It makes outsider hypotheses legible to expertise.

![Process overview](assets/epistemic_gap_mapper_process_overview.png)

## Core idea

Most review systems ask whether a manuscript fits an existing disciplinary frame. Epistemic Gap Mapper asks a different question:

> Where exactly does this hypothesis inherit from existing papers, where does it challenge a diffuse narrative, and where does it overreach?

The system separates:

- **Paper conflict**: disagreement with a specific source.
- **Narrative conflict**: disagreement with a standard story that may not be traceable to one strong paper.
- **Scope gap**: something target papers do not address.
- **Frame conflict**: a different interpretation of accepted evidence.
- **Overclaim**: a claim stronger than its evidence.

## Main workflow

1. **Input**
   - User manuscript / hypothesis.
   - Target papers.
   - Target narratives.

2. **Node extraction**
   - Extract Claim, Evidence, Paper, Narrative, Gap, Exception, Falsifier, and Method nodes.

3. **AI-assisted calibration**
   - Propose A/B/C/X tiers.
   - Separate papers from narratives.
   - Detect overclaims.
   - Mark comparisons as heuristic analogies, not evidence.

4. **Cross-frame diagnosis**
   - Check logic, source validity, paper relations, narrative debt, and unexplained exceptions.

5. **Output**
   - Node graph.
   - Inline manuscript annotations.
   - Breakthrough Diagnosis.
   - Narrative Audit.

## A/B/C/X claim tiers

| Tier | Meaning |
|---|---|
| A | Relatively strong claim supported by existing data or scholarship. |
| B | Plausible hypothesis consistent with current evidence but not proven. |
| C | Not yet assertable, but testable or worth preserving as a research question. |
| X | Unsupported, overclaimed, internally inconsistent, or contradicted by evidence. |
| M | Methodological tag or heuristic analogy, not direct evidence. |

## Recommended use

This skill is useful when a researcher, independent scholar, journalist, graduate student, or interdisciplinary team has a bold hypothesis and needs to know:

- which claims are actually supported,
- which claims are merely plausible,
- which claims must be weakened,
- which standard narrative is being challenged,
- and what evidence would falsify the hypothesis.

## Repository contents

- `SKILL.md` — Codex skill instructions and trigger metadata.
- `agents/openai.yaml` — UI metadata for skill lists and default invocation.
- `README.md` and `QUICKSTART.md` — public overview and usage flow.
- `CONTRIBUTING.md` — contribution rules and safety expectations.
- `docs/` — conceptual design, workflow, node schema, edge schema, methodological index.
- `prompts/` — copy-paste prompts for each step of the workflow.
- `schemas/` — JSON schemas for nodes, edges, and reports.
- `templates/` — reusable intake and report templates.
- `examples/` — worked example based on the Jomon/Dotaku/Kiki hypothesis.
- `outreach/` — public explainers and recruitment/community posts in English and Japanese.
- `scripts/` — lightweight local graph validation and Mermaid rendering helper.
- `assets/` — diagram and visual materials.

## License

Text, prompts, templates, and diagrams are intended for release under **CC BY 4.0 International** unless otherwise stated.

Executable helper scripts are intended for release under the **MIT License**. Text assets are intended for **CC BY 4.0**.

## v0.2 Additions

This package now includes outward-facing explanation and recruitment materials in `outreach/`, plus a prose-only case study for the Jomon / Dotaku / Kiki hypothesis in `examples/jomon_dotaku_kiki/prose_case/`.

The prose case is included because some preprint servers and scholarly venues reject bullet-heavy working papers as insufficiently formal or AI-like. The sample demonstrates how the same hypothesis can be written in complete formal prose, while the node decomposition walkthrough demonstrates how Epistemic Gap Mapper can recover the underlying claim structure afterward.
