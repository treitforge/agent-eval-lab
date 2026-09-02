# Examples

These examples use synthetic data. They do not contain an active evaluation case.

## One trajectory

`trajectories/atif-toy.json` contains a short ATIF run. The first test call fails. The same call later succeeds.

Analyze the file with this command:

```powershell
uv run trajectory-facts examples/trajectories/atif-toy.json
```

The report counts one explicit failed result. It also counts one failure-then-success group. It does not classify the result as an agent mistake.

## Offline comparison dashboard

`sample-harbor-job/` contains two synthetic Harbor trials. Both trials have a reward of `1.0`. The recorded processes are different.

```powershell
uv run trajectory-dashboard `
  --job examples/sample-harbor-job `
  --output .runs/sample-dashboard
```

This example does not require Docker, Harbor, model access, or credentials.

## Live public Harbor task

`harbor-toy-task/` contains a small Python project with a state defect. The defect occurs across upload batches. The project has public tests and a verifier.

Harbor hides the verifier from the agent container during the agent turn. This public repository still contains the verifier source.

Run the task with `scripts/run_toy_e2e.ps1`. See `docs/harbor-workflow.md` for the requirements and data flow.

This task is a teaching fixture. Do not use it to compare model capability.
