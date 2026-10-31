# Atlas Contributor Onboarding

Baseline: atlas-r1
Domain: docs-r1
Task: task-r1

1. Read the [project baseline](../AGENTS.md) and ask the assistant to read it
   in the selected Atlas workspace. Confirm atlas-r1 and its constraints.
   If native access is unavailable, supply the complete baseline text and
   identify it as a snapshot.
   Expected result: you can state the project purpose and output policy.

2. Supply the [documentation rules](../context/documentation.md) and
   [task brief](../tasks/onboarding.md) to your assistant.
   Request explicit file-tool reads and inspect the results. If access is
   unavailable, supply the complete required source text as snapshots.
   Expected result: the assistant identifies docs-r1 and task-r1 and names
   any missing source. Markdown links alone do not load these files.

3. Check the draft against the task acceptance criteria.
   Inspect the three steps, expected results, links, and final checklist.
   Expected result: each criterion has a recorded pass or a specific issue.

## Verification checklist
- [ ] Baseline and source revisions match the supplied documents.
- [ ] There are exactly three ordered steps with expected results.
- [ ] Relative links point to the intended files.
- [ ] Every task acceptance criterion has been checked.
