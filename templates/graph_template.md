# Graph Template

Copy this Mermaid skeleton and replace the labels.

```mermaid
graph TD
  P1[Target paper or source] -- supports --> E1[Evidence]
  E1 -- supports_weakly --> UC1[User claim]
  UC1 -- challenges_narrative --> N1[Target narrative]
  R1[Risk or overclaim] -. qualifies .-> UC1
  F1[Falsifier] -. falsified_by .-> UC1
  M1[Method or analogy] -. heuristic_analogy_for .-> UC1
```

Solid arrows usually show source, evidence, or inference structure.
Dotted arrows usually show risks, falsifiers, and heuristic or methodological relations.
