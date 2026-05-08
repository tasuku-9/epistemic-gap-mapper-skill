# Edge Schema

Edges describe the relation between nodes.

## Allowed edge relations

| Relation | Meaning |
|---|---|
| `supports` | Strongly supports another node. |
| `supports_weakly` | Supports as a plausible but non-decisive inference. |
| `contradicts` | Directly contradicts another node. |
| `extends` | Extends a source claim or frame beyond its original scope. |
| `qualifies` | Adds limits or qualifications. |
| `depends_on` | Requires another node as a premise. |
| `explains_gap` | Offers an explanation for a gap. |
| `challenges_narrative` | Challenges or reframes a Narrative Node. |
| `overclaims` | Exceeds what the supporting evidence permits. |
| `requires_test` | Requires future testing. |
| `falsified_by` | Is weakened or falsified by a Falsifier Node. |
| `heuristic_analogy_for` | Provides a comparison or analogy, not direct evidence. |
| `not_direct_evidence` | Explicitly marks a node as non-evidentiary. |

## Critical distinction

Comparative cases must use `heuristic_analogy_for`, not `supports`.

Example:

```text
Kumulipo oral genealogy example --heuristic_analogy_for--> Myth as ritual-political memory method
```

Not:

```text
Kumulipo --supports--> Kiki historical interpretation
```

## Optional local claim-evidence metadata

Use these fields when Stage 5C inspects whether a cited source locally supports a declared claim.

| Field | Allowed values |
|---|---|
| `support_strength` | `direct`, `hedged`, `presupposed`, `contextual`, `counter_example`, `analogy_only`, `no_direct_support`, `unknown` |
| `support_mode` | `empirical`, `textual`, `inferential`, `methodological`, `comparative`, `narrative_trace` |
| `source_span` | page, passage, figure, table, source node, or `not specified` |
| `local_check_status` | `pass`, `warn`, `fail`, `needs_source` |
| `claim_scope_match` | `full`, `partial`, `mismatch`, `unknown` |
| `vocabulary_match` | `same_terms`, `mapped_terms`, `ambiguous`, `mismatch` |
| `granularity_match` | `same_grain`, `too_broad`, `too_narrow`, `atomized`, `unknown` |

These fields are local checks only. They do not produce a global truth verdict.
