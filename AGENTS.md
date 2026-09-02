# Agent Eval Lab contributor instructions

Use ASD-STE100 Simplified Technical English for documentation.

## Purpose

This repository contains fact-only tools for coding-agent evaluations. The tools extract evidence from run artifacts. They do not replace human evaluation.

## Required behavior

- Preserve source references for each reported event.
- Use an explicit status field to count a failure or success.
- Keep raw result counts separate from human judgments.
- State when a source does not provide a timestamp, status, cost, token count, or duration.
- Prefer ATIF or OTLP over a vendor-specific format when both are available.
- Add a deterministic fixture for every adapter change.
- Keep generated reports and raw trajectories out of Git.
- Remove credentials and private data from fixtures and examples.

## Human decision boundary

Do not make these decisions for a human evaluator:

- Do not assign a model rating or severity.
- Do not select a winning model.
- Do not select a failure mode.
- Do not write a submission-ready preference explanation.
- Do not infer private chain-of-thought.

You can count observable events. You can group facts under an evaluation axis. You can check whether a human-written claim is supported by a cited event.

## Public task boundary

The task at `examples/harbor-toy-task/` is a teaching fixture. Its instruction and verifier are public by design. Do not present it as a valid benchmark.

Do not add an active evaluation prompt, private test data, a hidden verifier, an expected patch, or a raw private trajectory to this repository. Keep active evaluation cases in a separate private repository.

## Development checks

Run all checks before a commit:

```powershell
uv sync --all-groups
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Repository structure

- `src/trajectory_facts/`: adapters, normalization, analysis, reports, and dashboard.
- `tests/`: deterministic unit and public-example tests.
- `.codex/skills/trajectory-facts/`: reusable fact-analysis skill.
- `docs/`: architecture, evidence, format, and safety documentation.
- `examples/trajectories/`: small synthetic input files.
- `examples/sample-harbor-job/`: a synthetic job for offline dashboard use.
- `examples/harbor-toy-task/`: a public non-benchmark Harbor task.
- `scripts/`: task preparation and end-to-end example runners.
- `design/`: dashboard interface rules and tokens.

## File rules

- Use UTF-8 text.
- Use LF line endings except for PowerShell files.
- Use Python 3.11 or later.
- Keep runtime dependencies in the Python standard library when possible.
- Use `pathlib.Path` for paths.
- Do not log a token, password, private key, or authentication file content.
