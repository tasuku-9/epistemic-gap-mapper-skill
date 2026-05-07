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
