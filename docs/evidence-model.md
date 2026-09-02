# Evidence model

The project reports observable facts. A human decides what those facts mean.

## Explicit failed result

The source has a nonzero return code, an error status, or an error flag.

A failed result is not always an agent mistake. It can be a reproduction, negative test, optional-tool failure, or harness failure.

## Explicit successful result

The source has a zero return code or a success status.

The analyzer reports an unknown status when the source has no status. It does not convert missing data to success.

## Exact repeated call

Two or more calls have the same tool name and serialized arguments.

Similar commands are not exact repeated calls. A human can review similar commands separately.

## Failure then success

An exact call fails and a later copy succeeds.

This fact identifies a recovery sequence. It does not classify the quality of the recovery.

## Evaluation-axis groups

The analyzer groups evidence for review. It does not assign a rating.

| Axis | Machine-observable facts |
| --- | --- |
| Agentic Workflow | Command order, tool selection, exact repeats, failure and recovery sequences, run time |
| Instruction Following | Explicit instructions and matching recorded actions, when both are available |
| Core Functionality | Build, test, reproduction, runtime, and verifier results |
| Code Efficiency | Measured performance, resource use, algorithm facts, and benchmark results |
| Coding Style | Formatter, linter, type-checker, and repository-convention results |
| Effective Use of Codebase Context | Files, symbols, tests, documents, and searches that the agent inspected |
| Final Response Presentation | Final-response length, structure, verification claims, changed files, and stated limits |

Do not use an agent step count as a code-efficiency fact. Do not use intermediate commentary as a final-response fact.

Do not count a harness sentinel as an agent error without evidence that the agent caused it.

## Source references

Each event contains a source reference. An example is `steps[2] (step 3)`. Use this reference to check a claim in the source file.

Keep excerpts short. Remove secrets and private data before you share a report.
