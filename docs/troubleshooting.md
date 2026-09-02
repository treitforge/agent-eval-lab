# Troubleshooting

## The dashboard cannot find a trajectory

Agent Eval Lab first searches for `agent/trajectory.json`. Some Harbor versions can finish a trial but fail to convert the trajectory to ATIF.

When no ATIF file exists, Agent Eval Lab searches the native session directory for a supported JSONL file.

Keep the native session files until you build the report. Check `provenance.format` in the report to identify the adapter.

## Codex returns an authentication error

Confirm that Codex works in the WSL distribution that runs Harbor. Use `-CodexAuthJson` to pass the WSL path to the authentication file.

Do not copy the authentication file into the task or repository.

## Docker reports a credential-helper error

The example runner uses `examples/docker-public-config/config.json`. This configuration does not use a host credential helper for public image pulls.

If Docker Desktop reports concurrent helper errors, run the trials one at a time.

Do not add private registry credentials to the example configuration.

## A Windows path does not work in Harbor

Harbor runs in WSL in this example. The PowerShell runner converts `C:\work\repo` to `/mnt/c/work/repo`.

The runner rejects a path that does not have a local drive letter.

## The analyzer reports an unknown status

The source event has no explicit result status. The analyzer does not infer a status from result text.

Check the producer export. If the format has a documented status field, add the field to its adapter.

## The token or time fields are unavailable

Not every producer records timestamps, tool durations, tokens, or costs. The analyzer reports only available fields. It does not estimate missing values.

## The toy verifier is visible

The public task is a teaching fixture. Its verifier is public.

For an active evaluation, keep the verifier in a private repository. Make it available only during the verifier phase.
