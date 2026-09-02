"""Adapters for standard and common tool-specific trajectory exports."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .models import RunRecord, StepRecord, ToolEvent


class TrajectoryFormatError(ValueError):
    """Raised when no adapter can read the supplied document."""


def _content_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                if str(item.get("type", "")).lower() in {
                    "text",
                    "input_text",
                    "output_text",
                }:
                    parts.append(str(item.get("text", "")))
                elif "content" in item:
                    parts.append(_content_text(item["content"]))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(part for part in parts if part)
    if isinstance(value, dict):
        for key in (
            "aggregated_output",
            "formatted_output",
            "stdout",
            "output",
            "content",
            "message",
            "text",
        ):
            if key in value:
                return _content_text(value[key])
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _to_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _outcome(value: Any) -> tuple[int | None, bool | None, str]:
    """Read only explicit status fields. Do not infer failure from prose."""

    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith(("{", "[")):
            try:
                return _outcome(json.loads(stripped))
            except json.JSONDecodeError:
                pass
        return None, None, value

    if isinstance(value, list):
        outcomes = [_outcome(item) for item in value]
        return_codes = [item[0] for item in outcomes if item[0] is not None]
        failures = [item[1] for item in outcomes if item[1] is not None]
        return_code = next((code for code in return_codes if code != 0), None)
        if return_code is None and return_codes:
            return_code = 0
        failed = True if True in failures else (False if failures else None)
        return return_code, failed, _content_text(value)

    if not isinstance(value, dict):
        return None, None, _content_text(value)

    return_code = None
    for key in ("returncode", "return_code", "exit_code", "exitCode"):
        if key in value:
            return_code = _to_int(value[key])
            break

    explicit_error = None
    for key in ("isError", "is_error", "error"):
        if isinstance(value.get(key), bool):
            explicit_error = bool(value[key])
            break

    failed = (return_code != 0) if return_code is not None else explicit_error
    text = _content_text(value)

    if return_code is None and explicit_error is None:
        for key in ("content", "result", "output"):
            if key in value:
                nested_code, nested_failed, nested_text = _outcome(value[key])
                if nested_code is not None or nested_failed is not None:
                    return nested_code, nested_failed, nested_text

    return return_code, failed, text


def _read_document(path: Path) -> tuple[Any, str]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text), "json"
    except json.JSONDecodeError as json_error:
        values: list[Any] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                values.append(json.loads(line))
            except json.JSONDecodeError as line_error:
                raise TrajectoryFormatError(
                    f"Invalid JSON at line {line_number}: {line_error.msg}"
                ) from json_error
        if not values:
            raise TrajectoryFormatError("The trajectory file is empty") from json_error
        return values, "jsonl"


def _step_message(step: dict[str, Any]) -> str:
    return _content_text(step.get("message", step.get("content", "")))


def _atif(data: dict[str, Any], path: Path) -> RunRecord:
    agent = data.get("agent") or {}
    run = RunRecord(
        source_path=str(path),
        format_name="atif",
        schema_version=str(data.get("schema_version", "")) or None,
        session_id=str(data.get("session_id", "")) or None,
        agent_name=str(agent.get("name", "")) or None,
        agent_version=str(agent.get("version", "")) or None,
        model_name=str(agent.get("model_name", "")) or None,
        metrics=dict(data.get("final_metrics") or {}),
    )

    for index, step in enumerate(data.get("steps") or []):
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("step_id", index + 1))
        reference = f"steps[{index}] (step {step_id})"
        timestamp = step.get("timestamp")
        run.steps.append(
            StepRecord(
                reference=reference,
                step_id=step_id,
                source=str(step.get("source", "unknown")),
                timestamp=str(timestamp) if timestamp else None,
                message=_step_message(step),
            )
        )

        calls = [call for call in (step.get("tool_calls") or []) if isinstance(call, dict)]
        observation = step.get("observation") or {}
        results = observation.get("results") if isinstance(observation, dict) else []
        results = [item for item in (results or []) if isinstance(item, dict)]
        by_id = {
            str(item.get("source_call_id")): item
            for item in results
            if item.get("source_call_id") is not None
        }

        used_results: set[int] = set()
        for call_index, call in enumerate(calls):
            call_id = str(call.get("tool_call_id", "")) or None
            result = by_id.get(call_id or "")
            if result is None and call_index < len(results):
                result = results[call_index]
                used_results.add(call_index)
            elif result is not None:
                used_results.add(results.index(result))
            code, failed, result_text = _outcome(result or {})
            run.tool_events.append(
                ToolEvent(
                    reference=f"{reference}.tool_calls[{call_index}]",
                    step_id=step_id,
                    tool_name=str(call.get("function_name", "unknown")),
                    arguments=call.get("arguments") or {},
                    timestamp=str(timestamp) if timestamp else None,
                    result_text=result_text,
                    return_code=code,
                    failed=failed,
                    duration_ms=_duration_ms(result),
                    call_id=call_id,
                )
            )

        for result_index, result in enumerate(results):
            if result_index in used_results:
                continue
            code, failed, result_text = _outcome(result)
            run.tool_events.append(
                ToolEvent(
                    reference=f"{reference}.observation.results[{result_index}]",
                    step_id=step_id,
                    tool_name="observation",
                    timestamp=str(timestamp) if timestamp else None,
                    result_text=result_text,
                    return_code=code,
                    failed=failed,
                    duration_ms=_duration_ms(result),
                )
            )
    return run


def _duration_ms(value: Any) -> float | None:
    if not isinstance(value, dict):
        return None
    candidates = [value, value.get("extra")]
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        for key in ("duration_ms", "durationMs"):
            if key in candidate:
                try:
                    return float(candidate[key])
                except (TypeError, ValueError):
                    return None
    return None


def _swe_agent(data: dict[str, Any], path: Path) -> RunRecord:
    raw_info = data.get("info")
    info: dict[str, Any] = raw_info if isinstance(raw_info, dict) else {}
    raw_model_stats = info.get("model_stats")
    model_stats: dict[str, Any] = raw_model_stats if isinstance(raw_model_stats, dict) else {}
    run = RunRecord(
        source_path=str(path),
        format_name="swe-agent-traj",
        model_name=str(info.get("model_name", "")) or None,
        metrics=dict(model_stats),
    )
    for index, item in enumerate(data.get("trajectory") or []):
        if not isinstance(item, dict):
            continue
        step_id = str(index + 1)
        reference = f"trajectory[{index}] (step {step_id})"
        timestamp = item.get("timestamp")
        run.steps.append(
            StepRecord(
                reference=reference,
                step_id=step_id,
                source="agent",
                timestamp=str(timestamp) if timestamp else None,
                message=_content_text(item.get("response", item.get("thought", ""))),
            )
        )
        action = item.get("action")
        if action is not None:
            code, failed, result_text = _outcome(item.get("observation"))
            run.tool_events.append(
                ToolEvent(
                    reference=f"{reference}.action",
                    step_id=step_id,
                    tool_name=str(item.get("tool_name", "action")),
                    arguments={"command": action} if isinstance(action, str) else action,
                    timestamp=str(timestamp) if timestamp else None,
                    result_text=result_text,
                    return_code=code,
                    failed=failed,
                )
            )
    return run


def _unwrap_native_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    if entry.get("type") in {"assistant", "user", "system"} and isinstance(
        entry.get("message"), dict
    ):
        return dict(entry["message"])
    if entry.get("type") in {"response_item", "event_msg"} and isinstance(
        entry.get("payload"), dict
    ):
        payload = dict(entry["payload"])
        payload.setdefault("timestamp", entry.get("timestamp"))
        return payload
    return entry


def _chat_messages(data: Any, path: Path, format_name: str) -> RunRecord:
    if isinstance(data, dict):
        messages = data.get("messages") or data.get("events") or []
        metrics = (
            dict((data.get("info") or {}).get("model_stats") or {})
            if isinstance(data.get("info"), dict)
            else {}
        )
        schema_version = str(data.get("trajectory_format", "")) or None
    else:
        messages = data
        metrics = {}
        schema_version = None

    run = RunRecord(
        source_path=str(path),
        format_name=format_name,
        schema_version=schema_version,
        metrics=metrics,
    )
    pending: dict[str, ToolEvent] = {}

    for index, raw_entry in enumerate(messages or []):
        if not isinstance(raw_entry, dict):
            continue
        entry = _unwrap_native_entry(raw_entry)
        if not isinstance(entry, dict):
            continue
        role = str(entry.get("role", entry.get("source", entry.get("type", "unknown"))))
        step_id = str(entry.get("step_id", index + 1))
        reference = f"messages[{index}] (step {step_id})"
        timestamp = entry.get("timestamp")
        content = entry.get("content", entry.get("message", entry.get("output", "")))
        run.steps.append(
            StepRecord(
                reference=reference,
                step_id=step_id,
                source=role,
                timestamp=str(timestamp) if timestamp else None,
                message=_content_text(content),
            )
        )

        for call_index, call in enumerate(entry.get("tool_calls") or []):
            if not isinstance(call, dict):
                continue
            raw_function = call.get("function")
            function: dict[str, Any] = raw_function if isinstance(raw_function, dict) else call
            call_id = str(call.get("id", call.get("tool_call_id", ""))) or None
            arguments = function.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {"command": arguments}
            event = ToolEvent(
                reference=f"{reference}.tool_calls[{call_index}]",
                step_id=step_id,
                tool_name=str(function.get("name", function.get("function_name", "unknown"))),
                arguments=arguments,
                timestamp=str(timestamp) if timestamp else None,
                call_id=call_id,
            )
            run.tool_events.append(event)
            if call_id:
                pending[call_id] = event

        if isinstance(content, list):
            for block_index, block in enumerate(content):
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    call_id = str(block.get("id", "")) or None
                    event = ToolEvent(
                        reference=f"{reference}.content[{block_index}]",
                        step_id=step_id,
                        tool_name=str(block.get("name", "unknown")),
                        arguments=block.get("input") or {},
                        timestamp=str(timestamp) if timestamp else None,
                        call_id=call_id,
                    )
                    run.tool_events.append(event)
                    if call_id:
                        pending[call_id] = event
                elif block.get("type") == "tool_result":
                    call_id = str(block.get("tool_use_id", ""))
                    pending_event = pending.get(call_id)
                    code, failed, text = _outcome(block)
                    if pending_event:
                        pending_event.return_code = code
                        pending_event.failed = failed
                        pending_event.result_text = text

        if role == "tool" or entry.get("type") in {
            "function_call_output",
            "tool_result",
        }:
            call_id = str(entry.get("tool_call_id", entry.get("call_id", entry.get("id", ""))))
            pending_event = pending.get(call_id)
            code, failed, text = _outcome(content)
            if pending_event:
                pending_event.return_code = code
                pending_event.failed = failed
                pending_event.result_text = text

        if entry.get("type") == "function_call":
            call_id = str(entry.get("call_id", entry.get("id", ""))) or None
            arguments = entry.get("arguments") or {}
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {"command": arguments}
            event = ToolEvent(
                reference=reference,
                step_id=step_id,
                tool_name=str(entry.get("name", "unknown")),
                arguments=arguments,
                timestamp=str(timestamp) if timestamp else None,
                call_id=call_id,
            )
            run.tool_events.append(event)
            if call_id:
                pending[call_id] = event

        if entry.get("type") == "item_completed" and isinstance(entry.get("item"), dict):
            item = entry["item"]
            item_type = str(item.get("type", ""))
            if item_type == "CommandExecution":
                raw_command = item.get("command")
                if (
                    isinstance(raw_command, list)
                    and len(raw_command) >= 3
                    and raw_command[-2] == "-lc"
                ):
                    command = str(raw_command[-1])
                elif isinstance(raw_command, list):
                    command = " ".join(str(part) for part in raw_command)
                else:
                    command = str(raw_command or "")
                duration = item.get("duration")
                duration_ms = None
                if isinstance(duration, dict):
                    seconds = duration.get("secs", 0)
                    nanoseconds = duration.get("nanos", 0)
                    try:
                        duration_ms = (float(seconds) * 1000) + (
                            float(nanoseconds) / 1_000_000
                        )
                    except (TypeError, ValueError):
                        duration_ms = None
                code, failed, result_text = _outcome(item)
                run.tool_events.append(
                    ToolEvent(
                        reference=f"{reference}.item",
                        step_id=step_id,
                        tool_name="exec_command",
                        arguments={"command": command},
                        timestamp=str(timestamp) if timestamp else None,
                        result_text=result_text,
                        return_code=code,
                        failed=failed,
                        duration_ms=duration_ms,
                        call_id=str(item.get("id", "")) or None,
                    )
                )
            elif item_type == "FileChange":
                changes = item.get("changes")
                run.tool_events.append(
                    ToolEvent(
                        reference=f"{reference}.item",
                        step_id=step_id,
                        tool_name="apply_patch",
                        arguments={
                            "files": sorted(changes) if isinstance(changes, dict) else []
                        },
                        timestamp=str(timestamp) if timestamp else None,
                        result_text="FileChange item completed",
                        failed=False,
                        call_id=str(item.get("id", "")) or None,
                    )
                )

        if entry.get("type") == "token_count" and isinstance(entry.get("info"), dict):
            info = entry["info"]
            total_usage = info.get("total_token_usage")
            if isinstance(total_usage, dict):
                run.metrics.update(total_usage)
            if info.get("model_context_window") is not None:
                run.metrics["model_context_window"] = info["model_context_window"]

    return run


def _openhands(data: dict[str, Any], path: Path) -> RunRecord:
    """Read common OpenHands event exports without inferring prose errors."""

    run = RunRecord(source_path=str(path), format_name="openhands-events")
    pending: dict[str, ToolEvent] = {}
    events = data.get("events") or []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("id", index + 1))
        reference = f"events[{index}] (event {event_id})"
        timestamp = event.get("timestamp")
        source = str(event.get("source", event.get("type", "unknown")))
        run.steps.append(
            StepRecord(
                reference=reference,
                step_id=event_id,
                source=source,
                timestamp=str(timestamp) if timestamp else None,
                message=_content_text(event.get("message", event.get("content", ""))),
            )
        )

        action = event.get("action")
        if action is not None:
            if isinstance(action, dict):
                tool_name = str(
                    action.get("name", action.get("action", action.get("type", "action")))
                )
                arguments = action.get("args", action.get("arguments", action))
            else:
                tool_name = str(action)
                arguments = event.get("args", event.get("arguments", {}))
            tool_event = ToolEvent(
                reference=f"{reference}.action",
                step_id=event_id,
                tool_name=tool_name,
                arguments=arguments,
                timestamp=str(timestamp) if timestamp else None,
                call_id=event_id,
            )
            run.tool_events.append(tool_event)
            pending[event_id] = tool_event

        observation = event.get("observation")
        if observation is not None:
            cause_id = str(
                event.get(
                    "cause",
                    event.get("cause_id", event.get("tool_call_id", "")),
                )
            )
            pending_event = pending.get(cause_id)
            code, failed, text = _outcome(event)
            if pending_event:
                pending_event.return_code = code
                pending_event.failed = failed
                pending_event.result_text = text
            else:
                run.tool_events.append(
                    ToolEvent(
                        reference=f"{reference}.observation",
                        step_id=event_id,
                        tool_name=str(observation),
                        timestamp=str(timestamp) if timestamp else None,
                        result_text=text,
                        return_code=code,
                        failed=failed,
                    )
                )
    return run


def _otlp_any_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    for key in (
        "stringValue",
        "boolValue",
        "intValue",
        "doubleValue",
        "bytesValue",
    ):
        if key in value:
            return value[key]
    if "arrayValue" in value:
        return [_otlp_any_value(item) for item in value["arrayValue"].get("values", [])]
    if "kvlistValue" in value:
        return _otlp_attributes(value["kvlistValue"].get("values", []))
    return value


def _otlp_attributes(values: Iterable[Any]) -> dict[str, Any]:
    attributes: dict[str, Any] = {}
    for item in values:
        if isinstance(item, dict) and "key" in item:
            attributes[str(item["key"])] = _otlp_any_value(item.get("value"))
    return attributes


def _otlp(data: Any, path: Path) -> RunRecord:
    documents = data if isinstance(data, list) else [data]
    run = RunRecord(source_path=str(path), format_name="otlp-json")
    span_index = 0
    starts: list[int] = []
    ends: list[int] = []

    for document in documents:
        if not isinstance(document, dict):
            continue
        for resource_group in document.get("resourceSpans") or []:
            resource = resource_group.get("resource") or {}
            resource_attrs = _otlp_attributes(resource.get("attributes") or [])
            if not run.agent_name:
                run.agent_name = str(resource_attrs.get("gen_ai.agent.name", "")) or None
            for scope_group in resource_group.get("scopeSpans") or []:
                for span in scope_group.get("spans") or []:
                    if not isinstance(span, dict):
                        continue
                    span_index += 1
                    step_id = str(span_index)
                    reference = f"resourceSpans span {span_index}"
                    attrs = _otlp_attributes(span.get("attributes") or [])
                    start_ns = _to_int(span.get("startTimeUnixNano"))
                    end_ns = _to_int(span.get("endTimeUnixNano"))
                    if start_ns is not None:
                        starts.append(start_ns)
                    if end_ns is not None:
                        ends.append(end_ns)
                    duration_ms = (
                        (end_ns - start_ns) / 1_000_000
                        if start_ns is not None and end_ns is not None
                        else None
                    )
                    status = span.get("status") or {}
                    status_code = _to_int(status.get("code"))
                    failed = (
                        True if status_code == 2 else (False if status_code == 1 else None)
                    )
                    tool_name = str(
                        attrs.get(
                            "gen_ai.tool.name",
                            attrs.get("gen_ai.operation.name", span.get("name", "span")),
                        )
                    )
                    run.steps.append(
                        StepRecord(
                            reference=reference,
                            step_id=step_id,
                            source="span",
                            message=str(span.get("name", "")),
                        )
                    )
                    run.tool_events.append(
                        ToolEvent(
                            reference=reference,
                            step_id=step_id,
                            tool_name=tool_name,
                            arguments=attrs,
                            result_text=str(status.get("message", "")),
                            return_code=status_code,
                            failed=failed,
                            duration_ms=duration_ms,
                            call_id=str(span.get("spanId", "")) or None,
                        )
                    )
    if starts and ends:
        run.metrics["trace_elapsed_seconds"] = (max(ends) - min(starts)) / 1_000_000_000
    return run


def _is_otlp(data: Any) -> bool:
    if isinstance(data, dict):
        return "resourceSpans" in data
    return (
        bool(data)
        and isinstance(data, list)
        and all(isinstance(item, dict) and "resourceSpans" in item for item in data)
    )


def detect_format(data: Any) -> str:
    if isinstance(data, dict) and str(data.get("schema_version", "")).startswith("ATIF-"):
        return "atif"
    if _is_otlp(data):
        return "otlp-json"
    if isinstance(data, dict) and isinstance(data.get("trajectory"), list):
        return "swe-agent-traj"
    if isinstance(data, dict) and str(data.get("trajectory_format", "")).startswith(
        "mini-swe-agent"
    ):
        return "mini-swe-agent"
    if isinstance(data, dict) and isinstance(data.get("messages"), list):
        return "native-chat"
    if isinstance(data, dict) and isinstance(data.get("events"), list):
        return "openhands-events"
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return "native-jsonl"
    raise TrajectoryFormatError("No supported trajectory adapter matched this document")


def load_run(path: str | Path, format_name: str = "auto") -> RunRecord:
    """Load a trajectory and normalize its observable records."""

    source = Path(path).expanduser().resolve()
    data, encoding = _read_document(source)
    selected = detect_format(data) if format_name == "auto" else format_name

    if selected == "atif":
        run = _atif(data, source)
    elif selected == "otlp-json":
        run = _otlp(data, source)
    elif selected == "swe-agent-traj":
        run = _swe_agent(data, source)
    elif selected in {
        "mini-swe-agent",
        "native-chat",
        "native-jsonl",
    }:
        run = _chat_messages(data, source, selected)
    elif selected == "openhands-events":
        run = _openhands(data, source)
    else:
        raise TrajectoryFormatError(f"Unsupported format: {selected}")

    run.notes.append(f"Input encoding: {encoding}")
    return run
