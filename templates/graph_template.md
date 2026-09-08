# Mermaid Graph

Generated from `nodes_template.json` using `scripts/egm_cli.py render`. Edit the JSON and regenerate the diagram together.

## Legend

| Relation | Meaning |
|---|---|
| `supports` | Proposed supporting relation; its local check status is shown separately. |
| `supports_weakly` | Proposed partial or non-decisive support, not proof. |
| `challenges_narrative` | Challenges or reframes a narrative, not necessarily a paper. |
| `qualifies` | Limits how strongly the target may be stated. |
| `falsified_by` | Claim points to a condition that would weaken it; the result has not necessarily occurred. |
| `heuristic_analogy_for` | Analogy or comparison, not evidence. |

Solid support arrows indicate a recorded local `pass`, not global truth. Dotted arrows indicate pending or non-passing support, limits, future falsifiers, or non-evidentiary relations. Read each label: dotted does not mean false. `proposed` tiers are not human declarations; `needs_source` means the local source check is pending.

```mermaid
graph TD
  P1["P1 A (proposed):<br/>Replace with what this source is."]
  E1["E1 A (proposed):<br/>Replace with a concrete observation<br/>or source-backed fact."]
  N1["N1:<br/>Replace with the standard narrative<br/>or common explanation being<br/>examined."]
  UC1["UC1:<br/>Replace with your hypothesis or<br/>claim."]
  R1["R1 X (proposed):<br/>Replace with the main overclaim or<br/>confounder risk."]
  F1["F1 M (proposed):<br/>Replace with evidence that would<br/>weaken or falsify the claim."]
  P1 -. "supports (needs_source)" .-> E1
  E1 -. "weakly supports (needs_source)" .-> UC1
  UC1 -. "challenges narrative" .-> N1
  R1 -. "qualifies" .-> UC1
  UC1 -. "would be weakened by" .-> F1
```
