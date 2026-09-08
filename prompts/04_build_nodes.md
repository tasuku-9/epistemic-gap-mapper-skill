# Prompt 04 — Build Nodes

```text
Using my manuscript claims, target papers, and target narratives, build an Epistemic Gap Mapper node graph.

Use these node types:

- PaperNode
- SourceClaimNode
- UserClaimNode
- EvidenceNode
- InferenceNode
- AssumptionNode
- NarrativeNode
- NarrativeTraceNode
- GapNode
- ExceptionNode
- RiskNode
- FalsifierNode
- MethodNode

Each node should include:

- node_id
- node_type
- text
- domain
- tier: A / B / C / X / M / unknown
- supporting_sources
- related_target_papers
- related_target_narratives
- risks
- falsifiers
- confidence: high / medium / low / unknown

Use these edge relations:

- supports
- supports_weakly
- contradicts
- extends
- qualifies
- depends_on
- explains_gap
- challenges_narrative
- overclaims
- requires_test
- falsified_by
- heuristic_analogy_for
- not_direct_evidence

Output:

1. Node list in JSON-like format.
2. Edge list in JSON-like format.
3. A simple Mermaid graph.

Rules:
- Read docs/audit_records.md. Use proposed_tier and a provisional status unless an explicit human declaration is supplied.
- Allow empty source lists; supplied references must resolve. Never fill missing evidence or approvals with invented records.
- Uninspected support links use needs_source and unknown support_strength, not pass.
- falsified_by points from the claim to its FalsifierNode. depends_on points from an inference to its premise.
- Comparative cases must be MethodNodes or heuristic analogies, not EvidenceNodes.
- Target narratives must not be PaperNodes.
- C claims are allowed. X claims require patching.
- Do not score the manuscript.
```
