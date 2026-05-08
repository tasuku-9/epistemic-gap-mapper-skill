# X-Tier Failure Modes

`X` should not mean only "bad" or "wrong." It should state how a claim breaks.

Use `failure_modes` on any node with `tier = X` or `declared_tier = X`. Use an array because overclaims often fail in more than one way.

## Allowed modes

| Failure mode | Meaning |
|---|---|
| `evidence_laundering` | Weak, indirect, anecdotal, or ambiguous evidence is rewritten as if it were strong direct evidence. |
| `analogy_inflation` | A comparison, metaphor, pattern match, or historical parallel is promoted into evidence. |
| `narrative_capture` | A local observation is absorbed into a large story that decides the interpretation before the evidence does. |
| `falsifier_removal` | The claim is protected from possible disconfirmation by moving standards, adding escape clauses, or refusing test conditions. |
| `citation_debt` | A repeated claim has weak, missing, circular, or untraced sourcing. |
| `scope_jump` | A narrow observation is used to support a much broader conclusion than the source can carry. |

## Use

Prefer node-specific failure modes:

```json
{
  "node_id": "R1",
  "node_type": "RiskNode",
  "tier": "X",
  "failure_modes": ["scope_jump", "analogy_inflation"],
  "failure_mode_notes": "The argument moves from a real local anomaly to a civilization-scale conclusion through analogy."
}
```

Do not use `failure_modes` to punish a claim for being heterodox. A claim should become `X` when it exceeds local source support, contradicts cited evidence, removes falsifiers, or depends on analogy/narrative/citation moves as if they were proof.

## Public Writing Use

For essays or public examples, these modes can make the "X" legible:

- The question may be real.
- The observation may be real.
- The local uncertainty may be real.
- The conclusion becomes `X` because a specific failure mode enters the chain.

This is the basis of the "疑問は本物、結論はX" framing.
