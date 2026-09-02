# Supported formats

Use a documented interchange or telemetry format when one is available. Agent Eval Lab also supports some native vendor exports.

## Interchange and telemetry formats

### Agent Trajectory Interchange Format

ATIF is the primary trajectory format. The adapter reads `schema_version`, `agent`, `steps`, `tool_calls`, `observation`, and `final_metrics`.

The adapter preserves the ATIF step number in each evidence reference.

- [ATIF specification](https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md)
- [Harbor trajectory documentation](https://harborframework.com/docs/agents/trajectory-format)

### OpenTelemetry Protocol JSON

The OTLP JSON adapter reads `resourceSpans`, `scopeSpans`, and `spans`. It uses explicit span status and duration fields.

The adapter reads `gen_ai.*` attributes when they are available.

- [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)
- [OTLP file exporter](https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/)

## Tool-specific formats

These formats are separate and do not use one common schema.

- SWE-agent `.traj` JSON with a `trajectory` array.
- Mini-SWE-Agent JSON with `trajectory_format` and `messages`.
- OpenAI-style chat JSON with messages, roles, tool calls, and tool results.
- Common native JSONL events from Codex and Claude Code.
- OpenHands event arrays.

Use the producer's Harbor ATIF conversion when it is available.

## Detection limits

Native exports can change without a schema version. Format detection reports the selected adapter.

Check the producer documentation and source event when an important field is missing.

Not every vendor export is a standard. Add an adapter and synthetic fixture when a new stable format is available.
