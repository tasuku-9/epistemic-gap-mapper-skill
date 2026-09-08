# Mermaid Graph

Generated from `nodes_sample.json` using `scripts/egm_cli.py render`. Edit the JSON and regenerate the diagram together.

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
  P1["P1 A (proposed):<br/>Sato et al. 2014, overview of<br/>Y-chromosome variation in modern<br/>Japanese males."]
  SC1["SC1:<br/>Sato et al. 2014 reports<br/>Y-chromosome haplogroup variation in<br/>modern Japanese..."]
  E1["E1 A (proposed):<br/>D1a2a/D-M55 persists at high<br/>frequency in modern Japanese male<br/>lineages."]
  EX1["EX1 B (proposed):<br/>High D1a2a/D-M55 frequency coexists<br/>with largely continental-derived<br/>autosoma..."]
  A1["A1 C (proposed):<br/>Y-chromosome asymmetry can preserve<br/>signals of sex-biased social<br/>structure or..."]
  I1["I1 B (proposed):<br/>Paternal-lineage asymmetry may<br/>reflect some form of social or<br/>reproductive ad..."]
  G1["G1 B (proposed):<br/>Autosomal ancestry models do not by<br/>themselves explain the<br/>social-historical ..."]
  UC1["UC1 B (proposed):<br/>Paternal-lineage asymmetry may<br/>indicate some form of social or<br/>reproductive a..."]
  N2["N2:<br/>D1a2a/D-M55 persistence is best<br/>understood as passive<br/>Jomon-associated survival."]
  P2["P2 A (proposed):<br/>Hudson 1992 on Yayoi ritual and<br/>dotaku context."]
  E2["E2 A (proposed):<br/>Dotaku ritual flourished and then<br/>ended in the Late Yayoi period."]
  UC2["UC2 B (proposed):<br/>The end of dotaku ritual may reflect<br/>social reorganization or network<br/>disrupt..."]
  N3["N3:<br/>Dotaku discontinuity is usually<br/>treated as internal ritual<br/>transformation or ..."]
  UC3["UC3 B (proposed):<br/>Kiki myths may preserve structures<br/>of ritual-political memory related<br/>to soci..."]
  N4["N4:<br/>Kiki mythic material is often<br/>treated as literary-theological<br/>tradition rathe..."]
  P3["P3 A (proposed):<br/>The Kojiki and Nihon Shoki contain<br/>mythic complexes involving descent,<br/>land t..."]
  R1["R1 X (proposed):<br/>Y-chromosome frequency alone cannot<br/>prove conquest or elite dominance."]
  R2["R2 X (proposed):<br/>Dotaku discontinuity alone cannot<br/>prove external disruption or<br/>political take..."]
  R3["R3 X (proposed):<br/>Kiki mythic structures cannot be<br/>read as literal historical record."]
  F1["F1 M (proposed):<br/>If representative Kofun elite<br/>burials do not show elevated<br/>D1a2a/D-M55 compar..."]
  F2["F2 M (proposed):<br/>If dotaku discontinuity is fully<br/>explained by local ritual<br/>transformation wit..."]
  F3["F3 M (proposed):<br/>If Kiki descent and land-transfer<br/>motifs are late literary<br/>constructions with..."]
  M7["M7 M (proposed):<br/>Comparative cases are possibility<br/>structures, not evidence for the<br/>Japanese c..."]
  P1 -. "supports (needs_source)" .-> SC1
  SC1 -. "supports (needs_source)" .-> E1
  E1 -. "supports (needs_source)" .-> EX1
  EX1 -. "challenges narrative" .-> N2
  I1 -. "depends on" .-> A1
  E1 -. "weakly supports (needs_source)" .-> I1
  I1 -. "weakly supports (needs_source)" .-> UC1
  UC1 -. "explains gap" .-> G1
  UC1 -. "challenges narrative" .-> N2
  R1 -. "qualifies" .-> UC1
  UC1 -. "would be weakened by" .-> F1
  P2 -. "supports (needs_source)" .-> E2
  E2 -. "weakly supports (needs_source)" .-> UC2
  UC2 -. "challenges narrative" .-> N3
  R2 -. "qualifies" .-> UC2
  UC2 -. "would be weakened by" .-> F2
  P3 -. "weakly supports (needs_source)" .-> UC3
  UC3 -. "challenges narrative" .-> N4
  R3 -. "qualifies" .-> UC3
  UC3 -. "would be weakened by" .-> F3
  M7 -. "heuristic analogy" .-> UC2
  M7 -. "heuristic analogy" .-> UC3
```
