# Contributing

Thank you for improving Agent Eval Lab.

## Before you start

Open an issue for a large change. Describe the trajectory producer, the available schema or documentation, and the facts that the adapter must preserve.

Do not attach a private trajectory to a public issue. Replace names, prompts, paths, repository content, tokens, and model output with synthetic values.

## Add or change an adapter

1. Add a small synthetic fixture to `tests/`.
2. Preserve the source event number or step number.
3. Read explicit return codes and error fields. Do not infer failure from prose.
4. Report missing data as unavailable.
5. Update `docs/formats.md`.
6. Run all development checks in `AGENTS.md`.

## Pull requests

Keep each pull request focused. Explain the input format and the observable behavior that changed. Include test output. Do not include private evaluation material.

By contributing, you agree that your contribution is available under the MIT License.
