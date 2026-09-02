# Supported trajectory formats

## Interchange and telemetry standards

### Agent Trajectory Interchange Format

ATIF is the first-class agent trajectory format. The analyzer reads the root `schema_version`, `agent`, `steps`, `tool_calls`, `observation`, and `final_metrics` fields. It preserves the ATIF step number in each evidence reference.

Specification: <https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md>

Harbor documentation: <https://www.harborframework.com/docs/agents/trajectory-format>

### OpenTelemetry Protocol JSON

The analyzer reads OTLP JSON trace data from `resourceSpans`, `scopeSpans`, and `spans`. It uses explicit span status and duration fields. It also reads `gen_ai.*` attributes when they are present.

OTLP specification: <https://opentelemetry.io/docs/specs/otlp/>

File exporter specification: <https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/>

## Tool-specific formats

These formats are not one shared standard. The analyzer uses separate adapters.

- SWE-agent `.traj` JSON with a `trajectory` array.
- Mini-SWE-Agent JSON with `trajectory_format` and `messages`.
- OpenAI-style chat JSON with `messages`, roles, tool calls, and tool results.
- Common native JSONL events from Codex and Claude Code.
- OpenHands-style event arrays. Prefer Harbor's ATIF conversion when it is available.

SWE-agent output documentation: <https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md>

Mini-SWE-Agent example format: <https://github.com/SWE-agent/mini-traj-web-browser>

## Detection limits

Native exports can change without a schema-version field. Auto-detection reports the selected adapter. Check the producer documentation and the source event when an important field is missing.

The analyzer does not claim that every vendor export is a standard. Add a new adapter and fixture when a new stable shape appears.
