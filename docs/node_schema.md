# Node Schema

Nodes represent the components of a hypothesis and its relation to existing scholarship.

## Node types

### Paper Node

A specific source, article, book, report, preprint, or primary text.

Required fields:

- `node_id`
- `node_type = PaperNode`
- `citation`
- `domain`
- `source_kind`
- `role`
- `verification_status`

### Source Claim Node

A claim actually made by a target paper.

Required fields:

- `node_id`
- `node_type = SourceClaimNode`
- `text`
- `source_paper`
- `domain`
- `confidence`

### User Claim Node

A claim made by the user's manuscript.

Required fields:

- `node_id`
- `node_type = UserClaimNode`
- `text`
- `tier`
- `domain`
- `supporting_sources`
- `related_target_papers`
- `related_target_narratives`
- `risks`
- `falsifiers`

Optional calibration and local-check metadata:

- `vocabulary_map`
- `definition_scope`
- `granularity_justification`
- `proposed_tier`
- `declared_tier`
- `tier_declared_by`
- `tier_declaration_ref`
- `tier_rationale`
- `tier_review_status`

Use `declared_tier` only when the tier has been declared by a human author, domain expert, reviewer, or operator. The LLM may propose candidate tiers, but the final tier must keep the human declaration visible.

See [Audit Records](audit_records.md) for the required approval record and state transitions. A template or role name alone is not a declaration. Without a declaration, `tier` is provisional. Empty source, narrative, and risk lists are valid unfinished work; dangling IDs are not.

Any UserClaimNode with `tier = C`, `proposed_tier = C`, or `declared_tier = C` must link to at least one `FalsifierNode`.

Any node with `tier = X`, `proposed_tier = X`, or `declared_tier = X` must include `failure_modes`.

### Evidence Node

An observation, dataset, source statement, or primary textual fact used as evidence.

`source` is a node ID or an array of node IDs. Use an empty array when no source is recorded, not a fabricated reference. `source_paper` elsewhere must identify one PaperNode.

Required fields:

- `node_id`
- `node_type = EvidenceNode`
- `text`
- `source`
- `domain`
- `tier`

### Inference Node

A reasoning step connecting evidence to a claim.

Required fields:

- `node_id`
- `node_type = InferenceNode`
- `text`
- `tier`
- `depends_on`
- `risks`

### Assumption Node

An unstated or partially stated premise required by the argument.

Required fields:

- `node_id`
- `node_type = AssumptionNode`
- `text`
- `tier`
- `risk_level`

### Narrative Node

A standard narrative, disciplinary habit, textbook story, AI-frequency summary, or common synthesis.

Required fields:

- `node_id`
- `node_type = NarrativeNode`
- `text`
- `source_status`
- `citation_debt`
- `component_claims`

### Narrative Trace Node

A neutral trace record for candidate sources that appear to support, partially support, or fail to directly support a target narrative.

Use this to make citation debt visible without treating missing or partial source support as proof that a narrative is false.

Required fields:

- `node_id`
- `node_type = NarrativeTraceNode`
- `text`
- `target_narrative`
- `source_paper`
- `trace_status`
- `citation_debt_effect`

### Gap Node

Something existing papers or narratives do not explain.

Required fields:

- `node_id`
- `node_type = GapNode`
- `text`
- `located_in`
- `importance`

### Exception Node

A fact, observation, or case that fits poorly within the target narrative.

Required fields:

- `node_id`
- `node_type = ExceptionNode`
- `text`
- `target_narrative`
- `source`

### Risk / Overclaim Node

A statement where the manuscript may exceed its evidence.

Required fields:

- `node_id`
- `node_type = RiskNode`
- `text`
- `risky_phrase`
- `why_risky`
- `suggested_patch`

If `tier = X`, also include:

- `failure_modes`
- `failure_mode_notes` (recommended explanation of the particular failure, not required by the schema)

### Falsifier Node

A condition that would weaken or falsify the hypothesis.

Required fields:

- `node_id`
- `node_type = FalsifierNode`
- `text`
- `would_weaken`
- `required_evidence`

Recommended `test_plan` fields: `measurement`, `weakening_result`, and `alternative_explanation`. A missing plan on a C claim's falsifier produces an audit warning. This node describes a possible test outcome, not evidence that the outcome has already occurred.

### Method Node

A methodological tag, such as abductive reasoning or heuristic analogy.

Required fields:

- `node_id`
- `node_type = MethodNode`
- `method_name`
- `text`
- `not_evidence = true`
