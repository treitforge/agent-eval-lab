# Supported formats

Agent Eval Lab prefers documented interchange and telemetry formats. It also provides best-effort adapters for common vendor exports.

## Interchange and telemetry formats

### Agent Trajectory Interchange Format

ATIF is the first-class agent trajectory format. The adapter reads `schema_version`, `agent`, `steps`, `tool_calls`, `observation`, and `final_metrics`. It preserves the ATIF step number in each evidence reference.

- [ATIF specification](https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md)
- [Harbor trajectory documentation](https://harborframework.com/docs/agents/trajectory-format)

### OpenTelemetry Protocol JSON

The OTLP JSON adapter reads `resourceSpans`, `scopeSpans`, and `spans`. It uses explicit span status and duration fields. It reads `gen_ai.*` attributes when they exist.

- [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)
- [OTLP file exporter](https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/)

## Tool-specific formats

These formats are separate. They do not share one standard.

- SWE-agent `.traj` JSON with a `trajectory` array.
- Mini-SWE-Agent JSON with `trajectory_format` and `messages`.
- OpenAI-style chat JSON with messages, roles, tool calls, and tool results.
- Common native JSONL events from Codex and Claude Code.
- OpenHands-style event arrays.

Prefer a producer's Harbor ATIF conversion when it is available.

## Detection limits

Native exports can change without a schema version. Auto-detection reports the selected adapter. Check the producer documentation and the source event when an important field is missing.

The project does not claim that every vendor export is a standard. Add a new adapter and a synthetic fixture when a stable new shape appears.
