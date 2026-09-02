# Agent Eval Lab

[![CI](https://github.com/treitforge/agent-eval-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/treitforge/agent-eval-lab/actions/workflows/ci.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Agent Eval Lab extracts verifiable facts from coding-agent runs. It does not assign ratings, select a winner, or write an evaluation.

Two agents can pass the same verifier but use different processes. One agent can make one change and pass. Another agent can make several failed changes before it passes. A final reward does not show this difference. Agent Eval Lab keeps the evidence for a human review.

## What it provides

- Adapters for ATIF, OTLP JSON, SWE-agent, Mini-SWE-Agent, native Codex and Claude JSONL, OpenAI-style chat exports, and OpenHands event exports.
- Exact counts for tool calls, explicit results, repeats, recoveries, tokens, time, and patch size.
- Source references for facts that need verification.
- A static comparison dashboard for Harbor jobs.
- A reusable Codex skill for fact-only trajectory analysis.
- A public Harbor toy task that shows the full workflow.
- A synthetic sample job that works without model credentials or Docker.

## The workflow

```mermaid
flowchart LR
    A[Task snapshot] --> B[One-shot agent run]
    B --> C[Independent verifier]
    B --> D[Trajectory export]
    C --> E[Harbor job]
    D --> E
    E --> F[Fact extraction]
    F --> G[Comparison dashboard]
    G --> H[Human evaluation]
```

The verifier measures the final behavior. The trajectory records the process. A human uses both sources for an evaluation.

## Quick start

Install [uv](https://docs.astral.sh/uv/). Clone this repository. Then run these commands:

```powershell
uv sync --all-groups
uv run python -m unittest discover -s tests -v
```

Analyze the included ATIF trajectory with this command:

```powershell
uv run trajectory-facts examples/trajectories/atif-toy.json
```

Create the included comparison dashboard with this command:

```powershell
uv run trajectory-dashboard `
  --job examples/sample-harbor-job `
  --output .runs/sample-dashboard
```

Open `.runs/sample-dashboard/index.html` in a browser. The sample data is synthetic and contains no private model output.

## Run the public Harbor toy task

The optional toy task runs two Codex models through Harbor. The script then builds a fact-only dashboard from the recorded trajectories.

```powershell
.\scripts\run_toy_e2e.ps1 `
  -Harbor /path/to/harbor `
  -CodexAuthJson /home/you/.codex/auth.json
```

The script keeps credentials outside the repository. It writes all run files to the ignored `.runs/` directory.

The verifier for the toy task is public. Therefore, do not use this task as a benchmark. Keep active evaluation material in a private repository.

## Command-line tools

### `trajectory-facts`

```powershell
uv run trajectory-facts <trajectory.json-or-jsonl> `
  --patch <optional.patch> `
  --json-output facts.json `
  --markdown-output facts.md
```

The analyzer reports a failed result only when the source has an explicit failure status. It does not classify the result as an agent mistake.

### `trajectory-dashboard`

```powershell
uv run trajectory-dashboard --job <harbor-job-directory> --output <report-directory>
```

The dashboard writes `index.html`, `comparison.json`, `comparison.md`, and one fact report for each trial.

## Documentation

- [Architecture](docs/architecture.md)
- [Evidence model](docs/evidence-model.md)
- [Supported formats](docs/formats.md)
- [Harbor workflow](docs/harbor-workflow.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Add a trajectory adapter](docs/adding-an-adapter.md)
- [Public and private data boundary](docs/security-and-publication.md)
- [Toy examples](examples/README.md)
- [Contributing](CONTRIBUTING.md)

The `design/` directory contains the dashboard interface rules.

## Project status

This project is an early public release. Native vendor formats can change without notice. Use ATIF or OTLP when the producer supports one. Keep a source fixture for each adapter behavior.

## License

Agent Eval Lab is available under the [MIT License](LICENSE).
