# Troubleshooting

## The dashboard cannot find a trajectory

Prefer `agent/trajectory.json` when Harbor produced ATIF. Some Harbor or adapter versions can finish a trial but fail during post-run ATIF conversion. Agent Eval Lab then searches the trial's native session directory for a supported JSONL export.

Keep the native session files until you build the report. Check the report's `provenance.format` field to see which adapter was used.

## Codex returns an authentication error

Confirm that Codex works in the same WSL distribution that runs Harbor. Pass the WSL path to the existing authentication JSON file with `-CodexAuthJson`. Do not copy the file into the task or repository.

## Docker reports a credential-helper error

The example runner uses `examples/docker-public-config/config.json`. This minimal configuration avoids a host credential helper for public image pulls. Run trials sequentially when Docker Desktop still reports concurrent helper errors.

Do not add private registry credentials to the example configuration.

## A Windows path does not work in Harbor

Harbor runs in WSL in the documented example. The PowerShell runner converts local drive paths such as `C:\work\repo` to `/mnt/c/work/repo`. It rejects paths that do not have a local drive letter.

## The analyzer reports an unknown status

The source event did not provide an explicit return code, success status, error status, or error flag. The analyzer does not infer a status from result text. Check the producer export or add a documented adapter field.

## The token or time fields are unavailable

Not every producer records timestamps, tool durations, tokens, or costs. The analyzer reports only fields that are present. It does not estimate missing values.

## The toy verifier is visible

This is intentional. The public task is a teaching fixture. In an active evaluation, keep the verifier in a private task repository and mount or upload it only for the verifier phase.
