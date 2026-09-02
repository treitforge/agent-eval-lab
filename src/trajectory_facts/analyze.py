"""Compute factual run statistics and evidence buckets."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import RunRecord, ToolEvent

_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)"
    r"(\s*[:=]\s*)([^\s,;\"']+)"
)
_BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_URL_CREDENTIALS = re.compile(r"(https?://)[^/@\s]+@")


def _redact(text: str) -> str:
    text = _SECRET_ASSIGNMENT.sub(r"\1\2[REDACTED]", text)
    text = _BEARER.sub("Bearer [REDACTED]", text)
    return _URL_CREDENTIALS.sub(r"\1[REDACTED]@", text)


def _one_line(text: str, limit: int = 220) -> str:
    line = next((part.strip() for part in text.splitlines() if part.strip()), "")
    line = re.sub(r"\s+", " ", _redact(line))
    return line if len(line) <= limit else f"{line[: limit - 1]}…"


def _arguments_text(arguments: Any) -> str:
    if isinstance(arguments, dict):
        for key in ("cmd", "command", "script", "input"):
            value = arguments.get(key)
            if isinstance(value, str):
                return value
        return json.dumps(arguments, ensure_ascii=False, sort_keys=True, default=str)
    if isinstance(arguments, str):
        return arguments
    return json.dumps(arguments, ensure_ascii=False, sort_keys=True, default=str)


def _call_key(event: ToolEvent) -> str:
    value = {
        "tool": event.tool_name,
        "arguments": event.arguments,
    }
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _signature(event: ToolEvent) -> tuple[str, str]:
    excerpt = _one_line(event.result_text)
    raw = f"{event.tool_name}|{event.return_code}|{excerpt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12], excerpt


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _command_categories(command: str) -> list[str]:
    lowered = command.lower()
    categories: list[str] = []
    patterns = {
        "style": r"\b(black|ruff|flake8|pylint|eslint|prettier|isort|mypy|pyright)\b",
        "test": r"\b(pytest|unittest|npm\s+test|pnpm\s+test|yarn\s+test|cargo\s+test|go\s+test|test\.sh)\b",
        "build": r"\b(docker\s+build|podman\s+build|cargo\s+build|go\s+build|npm\s+run\s+build|pnpm\s+build|mvn\s+.*package|gradle\s+.*build|make\s+all)\b",
        "benchmark": r"\b(benchmark|pytest-benchmark|hyperfine|criterion)\b",
        "context": r"^\s*(ls\b|find\b|rg\b|grep\b|cat\b|head\b|tail\b|sed\s+-n\b|git\s+(show|diff|log|status)\b)",
    }
    for name, pattern in patterns.items():
        if re.search(pattern, lowered):
            categories.append(name)
    return categories


def _event_fact(event: ToolEvent) -> dict[str, Any]:
    command = _arguments_text(event.arguments)
    signature_id, excerpt = _signature(event)
    return {
        "reference": event.reference,
        "step_id": event.step_id,
        "tool": event.tool_name,
        "return_code": event.return_code,
        "failed": event.failed,
        "duration_ms": event.duration_ms,
        "command_preview": _one_line(command),
        "result_excerpt": excerpt,
        "failure_signature": signature_id if event.failed else None,
        "command_categories": _command_categories(command),
    }


def summarize_patch(path: str | Path) -> dict[str, Any]:
    """Return structural facts from a unified diff."""

    patch_path = Path(path).expanduser().resolve()
    files: list[str] = []
    additions = 0
    deletions = 0
    hunks = 0
    for line in patch_path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                target = parts[3]
                files.append(target.removeprefix("b/"))
        elif line.startswith("@@"):
            hunks += 1
        elif line.startswith("+") and not line.startswith("+++"):
            additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1
    return {
        "path": str(patch_path),
        "files_changed": len(dict.fromkeys(files)),
        "files": list(dict.fromkeys(files)),
        "additions": additions,
        "deletions": deletions,
        "hunks": hunks,
    }


def analyze_run(run: RunRecord, patch_path: str | Path | None = None) -> dict[str, Any]:
    """Build a report that contains observations but no ratings."""

    role_counts = Counter(step.source for step in run.steps)
    event_facts = [_event_fact(event) for event in run.tool_events]
    failed_events = [event for event in event_facts if event["failed"] is True]
    successful_events = [event for event in event_facts if event["failed"] is False]
    unknown_events = [event for event in event_facts if event["failed"] is None]

    calls_by_key: dict[str, list[int]] = defaultdict(list)
    events_by_key: dict[str, list[ToolEvent]] = defaultdict(list)
    for index, event in enumerate(run.tool_events):
        key = _call_key(event)
        calls_by_key[key].append(index)
        events_by_key[key].append(event)

    exact_repeats: list[dict[str, Any]] = []
    recoveries: list[dict[str, Any]] = []
    for key, indexes in calls_by_key.items():
        if len(indexes) > 1:
            events = events_by_key[key]
            exact_repeats.append(
                {
                    "tool": events[0].tool_name,
                    "command_preview": _one_line(_arguments_text(events[0].arguments)),
                    "count": len(events),
                    "references": [event.reference for event in events],
                }
            )
        events = events_by_key[key]
        for failure_index, event in enumerate(events):
            if event.failed is not True:
                continue
            later_success = next(
                (
                    candidate
                    for candidate in events[failure_index + 1 :]
                    if candidate.failed is False
                ),
                None,
            )
            if later_success:
                recoveries.append(
                    {
                        "tool": event.tool_name,
                        "failed_reference": event.reference,
                        "successful_reference": later_success.reference,
                        "command_preview": _one_line(_arguments_text(event.arguments)),
                    }
                )
                break

    failure_signatures: dict[str, dict[str, Any]] = {}
    for failed_fact in failed_events:
        signature = str(failed_fact["failure_signature"])
        item = failure_signatures.setdefault(
            signature,
            {
                "signature": signature,
                "tool": failed_fact["tool"],
                "return_code": failed_fact["return_code"],
                "result_excerpt": failed_fact["result_excerpt"],
                "count": 0,
                "references": [],
            },
        )
        item["count"] += 1
        item["references"].append(failed_fact["reference"])

    timestamps = [
        parsed
        for parsed in (_parse_timestamp(step.timestamp) for step in run.steps)
        if parsed is not None
    ]
    elapsed_seconds = None
    if len(timestamps) >= 2:
        try:
            elapsed_seconds = (max(timestamps) - min(timestamps)).total_seconds()
        except TypeError:
            elapsed_seconds = None

    explicit_durations = [
        event.duration_ms for event in run.tool_events if event.duration_ms is not None
    ]
    agent_steps = [step for step in run.steps if step.source.lower() in {"agent", "assistant"}]
    final_step = agent_steps[-1] if agent_steps else None
    final_text = final_step.message if final_step else ""

    style_events = [event for event in event_facts if "style" in event["command_categories"]]
    core_events = [
        event for event in event_facts if set(event["command_categories"]) & {"test", "build"}
    ]
    benchmark_events = [
        event for event in event_facts if "benchmark" in event["command_categories"]
    ]
    context_events = [
        event for event in event_facts if "context" in event["command_categories"]
    ]
    short_circuit_events = [
        event
        for event, fact in zip(run.tool_events, event_facts, strict=True)
        if "&&" in _arguments_text(event.arguments)
    ]

    report: dict[str, Any] = {
        "report_kind": "trajectory-facts-v1",
        "provenance": {
            "source_path": run.source_path,
            "format": run.format_name,
            "schema_version": run.schema_version,
            "session_id": run.session_id,
            "notes": run.notes,
        },
        "agent": {
            "name": run.agent_name,
            "version": run.agent_version,
            "model": run.model_name,
        },
        "run_counts": {
            "steps": len(run.steps),
            "steps_by_source": dict(sorted(role_counts.items())),
            "tool_calls": len(run.tool_events),
            "explicit_success_results": len(successful_events),
            "explicit_failed_results": len(failed_events),
            "results_without_explicit_status": len(unknown_events),
            "unique_failure_signatures": len(failure_signatures),
            "exact_repeated_call_groups": len(exact_repeats),
            "failure_then_success_same_call_groups": len(recoveries),
        },
        "time": {
            "first_timestamp": min(timestamps).isoformat() if timestamps else None,
            "last_timestamp": max(timestamps).isoformat() if timestamps else None,
            "elapsed_seconds_from_timestamps": elapsed_seconds,
            "sum_explicit_tool_duration_ms": sum(explicit_durations)
            if explicit_durations
            else None,
            "explicit_tool_duration_count": len(explicit_durations),
        },
        "metrics": run.metrics,
        "failed_results": failed_events,
        "failure_signatures": list(failure_signatures.values()),
        "exact_repeated_calls": exact_repeats,
        "failure_then_success_same_call": recoveries,
        "axis_evidence": {
            "agentic_workflow": {
                "tool_calls": len(run.tool_events),
                "explicit_failed_results": len(failed_events),
                "exact_repeated_calls": exact_repeats,
                "failure_then_success_same_call": recoveries,
                "commands_with_short_circuit_and": [
                    {
                        "reference": event.reference,
                        "command_preview": _one_line(_arguments_text(event.arguments)),
                    }
                    for event in short_circuit_events
                ],
            },
            "instruction_following": {
                "instruction_steps_present": sum(
                    count
                    for source, count in role_counts.items()
                    if source.lower() in {"system", "user"}
                ),
                "automated_compliance_assessment": "not determined",
            },
            "core_functionality": {"test_and_build_events": core_events},
            "code_efficiency": {"benchmark_events": benchmark_events},
            "coding_style": {"style_tool_events": style_events},
            "effective_use_of_codebase_context": {
                "read_search_and_inspection_events": context_events
            },
            "final_response_presentation": {
                "reference": final_step.reference if final_step else None,
                "present": bool(final_text),
                "character_count": len(final_text),
                "line_count": len(final_text.splitlines()) if final_text else 0,
            },
        },
        "capability_evidence": {
            "codebase_comprehension_and_context_use": {
                "read_search_and_inspection_events": context_events
            },
            "code_quality_and_instruction_following": {
                "style_tool_events": style_events,
                "test_and_build_events": core_events,
                "instruction_compliance": "not determined",
            },
            "planning_and_long_horizon_consistency": {
                "exact_repeated_calls": exact_repeats,
                "commands_with_short_circuit_and_count": len(short_circuit_events),
            },
            "debugging_and_error_recovery": {
                "failed_results": failed_events,
                "failure_then_success_same_call": recoveries,
            },
            "solution_design_and_architectural_quality": {
                "automated_architectural_assessment": "not determined"
            },
        },
        "limits": [
            "A failed result is not automatically an agent mistake.",
            "Instruction compliance needs an explicit instruction-to-action comparison.",
            "Ratings, preferences, severity, and failure-mode decisions are outside this report.",
            "Native tool formats can omit status, timestamps, or metrics.",
        ],
    }
    if patch_path is not None:
        patch = summarize_patch(patch_path)
        report["patch"] = patch
        report["capability_evidence"]["solution_design_and_architectural_quality"][
            "patch_structure"
        ] = patch
    return report
