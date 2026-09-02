"""Render a concise factual Markdown report."""

from __future__ import annotations

from typing import Any


def _value(value: Any) -> str:
    if value is None:
        return "not available"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _cell(value: Any) -> str:
    return _value(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: dict[str, Any]) -> str:
    provenance = report["provenance"]
    counts = report["run_counts"]
    time = report["time"]
    agent = report["agent"]
    lines = [
        "# Trajectory facts",
        "",
        "> This report contains machine-observable facts. It does not assign ratings or failure modes.",
        "",
        "## Source",
        "",
        f"- File: `{provenance['source_path']}`",
        f"- Format: `{provenance['format']}`",
        f"- Schema: `{_value(provenance.get('schema_version'))}`",
        f"- Agent: `{_value(agent.get('name'))}`",
        f"- Model: `{_value(agent.get('model'))}`",
        "",
        "## Run counts",
        "",
        "| Fact | Value |",
        "| --- | ---: |",
    ]
    labels = {
        "steps": "Steps",
        "tool_calls": "Tool calls",
        "explicit_success_results": "Explicit successful results",
        "explicit_failed_results": "Explicit failed results",
        "results_without_explicit_status": "Results without explicit status",
        "unique_failure_signatures": "Unique failure signatures",
        "exact_repeated_call_groups": "Exact repeated-call groups",
        "failure_then_success_same_call_groups": "Failure-then-success groups",
    }
    for key, label in labels.items():
        lines.append(f"| {label} | {_cell(counts.get(key))} |")

    lines.extend(
        [
            "",
            "## Time",
            "",
            "| Fact | Value |",
            "| --- | ---: |",
            f"| First timestamp | {_cell(time.get('first_timestamp'))} |",
            f"| Last timestamp | {_cell(time.get('last_timestamp'))} |",
            f"| Elapsed seconds from timestamps | {_cell(time.get('elapsed_seconds_from_timestamps'))} |",
            f"| Sum of explicit tool durations (ms) | {_cell(time.get('sum_explicit_tool_duration_ms'))} |",
        ]
    )

    failed = report.get("failed_results") or []
    lines.extend(["", "## Explicit failed results", ""])
    if failed:
        lines.extend(
            [
                "| Reference | Tool | Return code | Result excerpt |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for event in failed:
            lines.append(
                f"| {_cell(event['reference'])} | {_cell(event['tool'])} | "
                f"{_cell(event['return_code'])} | {_cell(event['result_excerpt'])} |"
            )
    else:
        lines.append("No explicit failed result was present.")

    repeats = report.get("exact_repeated_calls") or []
    lines.extend(["", "## Exact repeated calls", ""])
    if repeats:
        lines.extend(
            [
                "| Tool | Count | References | Command preview |",
                "| --- | ---: | --- | --- |",
            ]
        )
        for item in repeats:
            lines.append(
                f"| {_cell(item['tool'])} | {_cell(item['count'])} | "
                f"{_cell(', '.join(item['references']))} | {_cell(item['command_preview'])} |"
            )
    else:
        lines.append("No exact repeated call was present.")

    final = report["axis_evidence"]["final_response_presentation"]
    lines.extend(
        [
            "",
            "## Final response facts",
            "",
            f"- Reference: `{_value(final.get('reference'))}`",
            f"- Present: `{final.get('present')}`",
            f"- Characters: `{final.get('character_count')}`",
            f"- Lines: `{final.get('line_count')}`",
        ]
    )

    if "patch" in report:
        patch = report["patch"]
        lines.extend(
            [
                "",
                "## Patch structure",
                "",
                f"- Files changed: `{patch['files_changed']}`",
                f"- Additions: `{patch['additions']}`",
                f"- Deletions: `{patch['deletions']}`",
                f"- Hunks: `{patch['hunks']}`",
                f"- Files: `{', '.join(patch['files']) or 'none'}`",
            ]
        )

    lines.extend(["", "## Limits", ""])
    lines.extend(f"- {item}" for item in report.get("limits") or [])
    return "\n".join(lines) + "\n"
