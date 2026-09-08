# Local Support Calibration

This example uses [a short fictional source](source.md). It is not a real dataset or a scientific claim about weekday visits.

- UC1 repeats the source within its scope: the local textual check passes.
- UC2 expands one site-day into a universal comparison: the local check fails with a scope jump.
- UC3 preserves a testable question without pretending it already has supporting evidence. F1 specifies a measurement, a weakening result, and an alternative explanation.
- NT1 shows why a Tuesday mention does not substantiate a busiest-day narrative. Missing support does not prove that narrative false.

All tiers are proposals. `checked_by` identifies an LLM inspection of the supplied text; there is no human declaration. `verified` means the fixture text was available for inspection, not that its fictional observation occurred.

Inspect `nodes_calibration.json` or [the generated graph](graph_calibration.md). The source excerpt and locator on each completed check make the finding traceable. `pass`, `warn`, and `fail` describe only that local check.
