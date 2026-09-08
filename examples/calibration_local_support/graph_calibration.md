# Mermaid Graph

Generated from `nodes_calibration.json` using `scripts/egm_cli.py render`. Edit the JSON and regenerate the diagram together.

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
  P1["P1:<br/>A fictional, single-site, single-day<br/>observation statement."]
  UC1["UC1 A (proposed):<br/>The fixture reports 12 visits at<br/>Site A on Tuesday."]
  UC2["UC2 X (proposed):<br/>All sites always receive more visits<br/>on Tuesdays than on other days."]
  UC3["UC3 C (proposed):<br/>At Site A, Tuesday visit counts may<br/>exceed other weekdays over repeated<br/>weeks."]
  N1["N1:<br/>Tuesdays are generally the busiest<br/>day."]
  NT1["NT1:<br/>The fixture mentions Tuesday but<br/>makes no weekday comparison."]
  R1["R1 X (proposed):<br/>A one-day count cannot establish a<br/>weekday advantage."]
  F1["F1:<br/>A matched multiweek comparison may<br/>fail to show the proposed Tuesday<br/>advantage."]
  P1 -- "supports (pass)" --> UC1
  P1 -. "supports (fail)" .-> UC2
  P1 -. "weakly supports (warn)" .-> NT1
  NT1 -. "not direct evidence" .-> N1
  R1 -. "qualifies" .-> UC2
  R1 -. "qualifies" .-> UC3
  UC3 -. "would be weakened by" .-> F1
```
