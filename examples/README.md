# Examples

The examples use synthetic data. They do not contain an active evaluation case.

## One trajectory

`trajectories/atif-toy.json` contains a short ATIF run. The first test call fails. The exact call later succeeds. Analyze it with:

```powershell
uv run trajectory-facts examples/trajectories/atif-toy.json
```

The report counts one explicit failed result and one failure-then-success group. It does not call the failed result an agent mistake.

## Offline comparison dashboard

`sample-harbor-job/` contains two synthetic Harbor trial directories. Both trials have a reward of `1.0`. Their recorded workflows differ.

```powershell
uv run trajectory-dashboard `
  --job examples/sample-harbor-job `
  --output .runs/sample-dashboard
```

This example needs no Docker, Harbor, model access, or credentials.

## Live public Harbor task

`harbor-toy-task/` contains a small Python project with a cross-batch state defect. The project has public tests and a verifier. The verifier is hidden from the agent container during the agent turn, but it is visible in this public repository.

Run it with `scripts/run_toy_e2e.ps1`. See `docs/harbor-workflow.md` for requirements and data flow.

This task is a teaching fixture. Do not use it to compare model capability.
