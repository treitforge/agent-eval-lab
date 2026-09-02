# Factual evidence taxonomy

Use this reference to group facts. Do not assign a rating or failure mode.

## Evaluation axes

### Agentic Workflow

Use command order, tool selection, repeated calls, failed-result sequences, recovery sequences, and run time. Do not use algorithm performance here.

### Instruction Following

Use an explicit instruction and its matching recorded action. If the artifacts do not contain the instruction, mark this axis as not determined.

### Core Functionality

Use builds, tests, reproduction output, runtime output, remaining defects, and final verification. State whether a result is temporary or final.

### Code Efficiency

Use algorithm complexity, redundant data passes, resource use, and benchmark output. Agent step count does not belong here.

### Coding Style

Use repository conventions and formatter, linter, type-checker, or review output. A runtime exception is not a coding-style fact.

### Effective Use of Codebase Context

Use files, searches, symbols, tests, and unsupported API assumptions that the agent inspected.

Do not use the same fact again as an Agentic Workflow defect.

### Final Response Presentation

Use only the final response. Record its structure, length, verification statement, changed-file statement, and stated limits.

## Capability areas

- **Codebase Comprehension and Context Use:** relevant paths, impact analysis, conventions, and API assumptions.
- **Code Quality and Instruction Following:** logic, explicit constraints, lint output, and ambiguity handling.
- **Planning and Long-Horizon Consistency:** dependency order, sequence, repeated failures, and broken intermediate states.
- **Debugging and Error Recovery:** reproduction, root-cause evidence, failed attempts, recovery, and abandonment.
- **Solution Design and Architectural Quality:** changed layers, duplicated logic, abstraction boundaries, and API contracts.

## Terms

- **Explicit failed result:** The artifact has a nonzero return code, error status, or error flag.
- **Exact repeated call:** The tool name and serialized arguments are equal.
- **Failure then success:** An exact repeated call fails and a later copy has an explicit success status.
- **Human-classified mistake:** A human attributes a failed result to the agent and selects its evaluation axis. The analyzer does not make this decision.
