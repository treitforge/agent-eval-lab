# Harbor workflow

The public toy task shows a complete Harbor workflow. It is a teaching fixture and not a benchmark.

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

The Docker image copies only `environment/codebase/` to `/app`. The agent works in `/app`.

Harbor makes the verifier files available at `/tests` after the agent turn.

This public repository contains all toy files. Keep verifier files and task data private during an active evaluation.

## Verifier behavior

The verifier runs deterministic tests. It writes `1` or `0` to `/logs/verifier/reward.txt`.

The verifier writes test output to `/logs/verifier/test-stdout.txt`.

A reward measures the tested behavior. It does not measure the agent process, architecture, code style, or final response.

## Run two models

Use the PowerShell runner on Windows. WSL, Docker, Harbor, and Codex must be available.

```powershell
.\scripts\run_toy_e2e.ps1 `
  -Distro Ubuntu `
  -Harbor /path/to/harbor `
  -CodexAuthJson /home/you/.codex/auth.json `
  -Models gpt-5.6-sol,gpt-5.6-luna
```

The runner does these operations:

1. It copies the public task to an ignored snapshot under `.runs/tasks/`.
2. It runs each model one time through the Harbor Codex agent.
3. Harbor runs the independent verifier after each agent turn.
4. Harbor records result metadata, patches, test output, and trajectories.
5. The runner builds a static fact-only dashboard under `.runs/reports/`.

The runner uses one agent at a time. This setting prevents some Docker Desktop credential-helper conflicts.

## Authentication

Pass only the WSL path to the Codex authentication JSON file. The script does not read, copy, or print the file.

Do not put the authentication file in this repository.

If the Harbor agent environment has Codex authentication, you can omit `-CodexAuthJson`.
