# Supported trajectory formats

## Interchange and telemetry standards

### Agent Trajectory Interchange Format

ATIF is the primary trajectory format. The analyzer reads `schema_version`, `agent`, `steps`, `tool_calls`, `observation`, and `final_metrics`.

The analyzer preserves the ATIF step number in each evidence reference.

Specification: <https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md>

Harbor documentation: <https://www.harborframework.com/docs/agents/trajectory-format>

### OpenTelemetry Protocol JSON

The analyzer reads OTLP JSON trace data from `resourceSpans`, `scopeSpans`, and `spans`. It uses explicit span status and duration fields.

The analyzer also reads available `gen_ai.*` attributes.

OTLP specification: <https://opentelemetry.io/docs/specs/otlp/>

File exporter specification: <https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/>

## Tool-specific formats

These formats do not use one common schema. The analyzer uses a separate adapter for each format.

- SWE-agent `.traj` JSON with a `trajectory` array.
- Mini-SWE-Agent JSON with `trajectory_format` and `messages`.
- OpenAI-style chat JSON with `messages`, roles, tool calls, and tool results.
- Common native JSONL events from Codex and Claude Code.
- OpenHands event arrays.

Use Harbor's ATIF conversion when it is available.

SWE-agent output documentation: <https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md>

Mini-SWE-Agent example format: <https://github.com/SWE-agent/mini-traj-web-browser>

## Detection limits

Native exports can change without a schema-version field. Format detection reports the selected adapter.

Check the producer documentation and source event when an important field is missing.

Not every vendor export is a standard. Add an adapter and fixture when a new stable format is available.
