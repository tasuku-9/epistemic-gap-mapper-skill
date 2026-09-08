# Mermaid Graph

Generated from `nodes_starter.json` using `scripts/egm_cli.py render`. Edit the JSON and regenerate the diagram together.

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
  P1["P1 A (proposed):<br/>A local cafe sales log containing<br/>daily revenue and transaction counts<br/>for th..."]
  P2["P2 A (proposed):<br/>A local weather log identifying<br/>which business days were rainy<br/>during the sal..."]
  SC1["SC1:<br/>The sales log can show whether<br/>average revenue or transaction count<br/>differs b..."]
  E1["E1 B (proposed):<br/>Rainy days in the sample appear to<br/>have higher average transaction<br/>counts tha..."]
  E2["E2 A (proposed):<br/>The rainy-day label comes from the<br/>local weather log for the same<br/>period."]
  N1["N1:<br/>Rainy days bring more people into<br/>cafes because customers want an<br/>indoor plac..."]
  NT1["NT1 M (proposed):<br/>The cafe sales log may be compatible<br/>with the rainy-day sales narrative,<br/>but ..."]
  UC1["UC1 B (proposed):<br/>Rainy days may increase this cafe&#x27;s<br/>sales, but the cause needs to be<br/>checked ..."]
  R1["R1 X (proposed):<br/>Rain may coincide with weekends,<br/>events, holidays, promotions, or<br/>seasonal ch..."]
  F1["F1 M (proposed):<br/>If the rainy-day effect disappears<br/>after controlling for weekends,<br/>events, pr..."]
  P1 -. "supports (needs_source)" .-> SC1
  SC1 -. "supports (needs_source)" .-> E1
  P2 -. "supports (needs_source)" .-> E2
  E1 -. "weakly supports (needs_source)" .-> UC1
  E2 -. "weakly supports (needs_source)" .-> UC1
  P1 -. "weakly supports (needs_source)" .-> NT1
  NT1 -. "not direct evidence" .-> N1
  UC1 -. "challenges narrative" .-> N1
  R1 -. "qualifies" .-> UC1
  UC1 -. "would be weakened by" .-> F1
```
