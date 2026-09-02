# Contributing

Thank you for your contribution to Agent Eval Lab.

## Before you start

Open an issue before you make a large change. Identify the trajectory producer and its version. Identify the facts that the adapter must preserve.

Do not attach a private trajectory to a public issue. Replace all private values with synthetic values.

## Add or change an adapter

1. Add a small synthetic fixture to `tests/`.
2. Preserve the source event or step number.
3. Read explicit return codes and error fields. Do not infer a status from prose.
4. Report missing data as unavailable.
5. Update `docs/formats.md`.
6. Run all development checks in `AGENTS.md`.

## Pull requests

Keep each pull request focused. Explain the input format and the changed behavior. Include the test output. Do not include private evaluation material.

By contributing, you agree that your contribution is available under the MIT License.
