# Harbor workflow

The public toy task shows one complete Harbor workflow. It is a teaching fixture, not a benchmark.

## Task contents

```text
examples/harbor-toy-task/
|-- instruction.md
|-- task.toml
|-- environment/
|   |-- Dockerfile
|   `-- codebase/
`-- tests/
    |-- test.sh
    `-- test_scan_ledger.py
```

The Docker image copies only `environment/codebase/` to `/app`. The agent works in `/app`. Harbor makes the verifier files available at `/tests` after the agent turn.

The public repository exposes all toy files for education. In an active evaluation, keep verifier files and task-specific data private.

## Verifier behavior

The verifier runs deterministic tests. It writes `1` or `0` to `/logs/verifier/reward.txt`. It also writes test output to `/logs/verifier/test-stdout.txt`.

A reward measures the tested behavior. It does not measure workflow quality, architecture, style, or final-response quality.

## Run two models

Use the supplied PowerShell runner from Windows with WSL, Docker, Harbor, and Codex available:

```powershell
.\scripts\run_toy_e2e.ps1 `
  -Distro Ubuntu `
  -Harbor /path/to/harbor `
  -CodexAuthJson /home/you/.codex/auth.json `
  -Models gpt-5.6-sol,gpt-5.6-luna
```

The runner performs these operations:

1. It copies the public task to an ignored snapshot under `.runs/tasks/`.
2. It runs each model once through the Harbor Codex agent.
3. Harbor runs the independent verifier after each agent turn.
4. Harbor records result metadata, patches, test output, and trajectories.
5. The runner builds a static fact-only dashboard under `.runs/reports/`.

The runner uses one concurrent agent. This avoids Docker credential-helper conflicts on some Docker Desktop installations.

## Authentication

Pass only the WSL path to the Codex authentication JSON file. The script does not read, copy, or print the file content. Never place the file in this repository.

You can omit `-CodexAuthJson` when Codex authentication is already available to the Harbor agent environment.
