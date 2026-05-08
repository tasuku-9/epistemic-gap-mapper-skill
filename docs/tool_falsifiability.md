# Tool Falsifiability

Epistemic Gap Mapper should itself remain falsifiable as a method.

The tool is failing if it repeatedly makes hypotheses less auditable, less locally sourced, or less legible to expert review.

## Failure conditions

Treat the mapper as failing, or at least needing redesign, when any of these patterns recur:

1. Known valid heterodox hypotheses are repeatedly pushed into `X` merely because they challenge a standard narrative.
2. Known false hypotheses are repeatedly preserved as `C` even after local source checks show no repairable support or no testable falsifier.
3. Tier distributions diverge heavily across trained operators using the same graph and evidence set.
4. Heuristic analogies, myths, comparisons, or methods are treated as direct evidence.
5. Target narratives collapse into target papers, making diffuse citation debt look like direct paper conflict.
6. Overclaims exceeding local source support are not detected.
7. X-tier nodes are labeled only as "bad" without `failure_modes`, making the breakage impossible to inspect.

## Calibration checks

Use periodic calibration sets:

- a small set of repaired heterodox claims that should remain inspectable,
- a small set of known overclaims that should be patched or marked `X`,
- a small set of analogy-only examples that must remain `M` or `heuristic_analogy_for`,
- a small set of narrative-audit examples where sources are compatible with a narrative but do not directly claim it.

Compare outputs across operators. Large disagreement is not automatically failure, but it is evidence that the workflow needs clearer definitions, better examples, or more local support metadata.

## What failure does not mean

Tool failure does not prove a target narrative false.

Tool failure does not prove a heterodox hypothesis true.

Tool failure means the mapper is not producing a reliable audit surface for human review.

## Repair path

When a failure condition appears:

1. Identify the smallest graph relation or prompt instruction causing the failure.
2. Add or revise a schema field only if it improves auditability.
3. Add a worked example before adding abstract rules.
4. Prefer local claim-evidence checks over global verdict language.
5. Re-run the calibration set with at least two human operators when possible.
