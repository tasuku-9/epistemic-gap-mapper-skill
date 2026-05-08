# Contributing

Epistemic Gap Mapper should be grown as a community asset.

## Good contributions

- New node schema refinements.
- New edge relation proposals.
- Better prompt wording.
- Worked examples from other domains.
- Better falsification-condition templates.
- Narrative audit examples.
- Visual graph renderers.

## Rules

1. Do not use the system to launder unsupported claims into scholarly-looking prose.
2. Do not classify speculative claims as A.
3. Do not treat comparisons as evidence.
4. Do not use “no source found” as proof that a narrative is false.
5. Preserve the distinction between target papers and target narratives.
6. Mark uncertainty explicitly.
7. Every worked example must include X-level risks.

## Adding a new case

Create a folder in `examples/` with:

- `input_summary.md`
- `target_papers.md`
- `target_narratives.md`
- `nodes_minimal.json`
- `nodes_full.json` when the case needs fuller coverage
- `breakthrough_diagnosis_sample.md`

## Adding a new method tag

Add it to `docs/methodological_index.md` and explain:

- what it permits,
- what it does not permit,
- when it should be used,
- and what overclaim it helps prevent.
