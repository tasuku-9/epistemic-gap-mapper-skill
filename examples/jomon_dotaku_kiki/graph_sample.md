# Sample Mermaid Graph

## Legend

| Relation | Meaning | Usual arrow style |
|---|---|---|
| `supports` | A source, source claim, or evidence node directly supports another node. | Solid arrow |
| `supports_weakly` | A node is consistent with or partially supports another node, but does not prove it. | Solid arrow, preferably labeled |
| `challenges_narrative` | A claim, exception, or model challenges or reframes a `NarrativeNode`. | Solid labeled arrow |
| `qualifies` | A risk or limitation constrains how strongly a claim may be stated. | Dotted arrow |
| `falsified_by` | A falsifier identifies evidence that would weaken a claim. | Dotted arrow |
| `heuristic_analogy_for` | A method or comparison supplies a possibility structure, not direct evidence. | Dotted arrow |

Solid arrows indicate evidentiary or inferential structure. Dotted arrows indicate limits, falsifiers, or heuristic/methodological relations.

```mermaid
graph TD
  P1[Sato et al. 2014] -- supports --> SC1[Source claim]
  SC1 -- supports --> E1[D1a2a/D-M55 high frequency]
  E1 -- supports_weakly --> EX1[Lineage/autosomal asymmetry exception]
  EX1 -- challenges_narrative --> N2[Passive survival narrative]
  A1[Social signal assumption] --> I1[Paternal asymmetry inference]
  I1 -- supports_weakly --> UC1[Possible paternal social advantage]
  UC1 -- explains_gap --> G1[Social-historical meaning gap]
  UC1 -- challenges_narrative --> N2
  R1[Y-DNA alone cannot prove dominance] -. qualifies .-> UC1
  F1[Kofun elite aDNA test] -. falsifies/weaken .-> UC1

  P2[Hudson 1992] -- supports --> E2[Dotaku ritual discontinuity]
  E2 -- supports_weakly --> UC2[Possible social reorganization]
  UC2 -- challenges_narrative --> N3[Internal-transformation-only narrative]
  R2[Dotaku discontinuity risk] -. qualifies .-> UC2
  F2[Local transformation test] -. falsifies/weaken .-> UC2

  P3[Kojiki / Nihon Shoki] -- supports_weakly --> UC3[Possible ritual-political memory]
  UC3 -- challenges_narrative --> N4[Myth as literary tradition narrative]
  R3[Myth is not chronicle] -. qualifies .-> UC3
  F3[Late construction test] -. falsifies/weaken .-> UC3
  M7[Heuristic comparative history] -. analogy only .-> UC2
  M7 -. analogy only .-> UC3
```
