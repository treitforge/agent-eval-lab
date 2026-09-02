# Evidence model

The project reports observable facts. A human decides what those facts mean.

## Terms

### Explicit failed result

The source has a nonzero return code, an error status, or an error flag.

An explicit failed result is not automatically an agent mistake. It can be an intentional reproduction, a negative test, a missing optional tool, or a harness failure.

### Explicit successful result

The source has a zero return code or a success status.

No status means unknown. The analyzer does not convert missing data to success.

### Exact repeated call

The tool name and serialized arguments are equal for two or more calls.

Similar commands are not exact repeats. A human can inspect them as repeat candidates.

### Failure then success

An exact call has an explicit failure and a later copy has an explicit success.

This fact shows a recovery sequence. It does not show whether the recovery was good or bad.

## Evaluation-axis routing

The analyzer groups evidence for review. It does not assign a rating.

| Axis | Machine-observable facts |
| --- | --- |
| Agentic Workflow | Command order, tool selection, exact repeats, failure and recovery sequences, run time |
| Instruction Following | Explicit instructions and matching recorded actions, when both exist |
| Core Functionality | Build, test, reproduction, runtime, and verifier results |
| Code Efficiency | Measured performance, resource use, algorithm facts, and benchmarks |
| Coding Style | Formatter, linter, type-checker, and repository-convention results |
| Effective Use of Codebase Context | Files, symbols, tests, documentation, and searches inspected |
| Final Response Presentation | Final-response length, structure, verification claims, changed files, and stated limits |

Do not use an agent step count as a code-efficiency fact. Do not use intermediate commentary as a final-response fact. Do not count a harness sentinel as an agent error without evidence that the agent caused it.

## Source citations

Every event contains a source reference such as `steps[2] (step 3)` or `messages[7] (step 8)`. Use that reference when you check a claim in the original file.

Keep excerpts short. Remove secrets and private data before you share a report.
