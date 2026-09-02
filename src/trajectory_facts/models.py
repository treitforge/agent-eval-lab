"""Normalized records used by all trajectory adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StepRecord:
    """One source step or message."""

    reference: str
    step_id: str
    source: str
    timestamp: str | None = None
    message: str = ""


@dataclass(slots=True)
class ToolEvent:
    """One tool call and its observed result, when available."""

    reference: str
    step_id: str
    tool_name: str
    arguments: Any = field(default_factory=dict)
    timestamp: str | None = None
    result_text: str = ""
    return_code: int | None = None
    failed: bool | None = None
    duration_ms: float | None = None
    call_id: str | None = None


@dataclass(slots=True)
class RunRecord:
    """A normalized trajectory run."""

    source_path: str
    format_name: str
    schema_version: str | None = None
    session_id: str | None = None
    agent_name: str | None = None
    agent_version: str | None = None
    model_name: str | None = None
    steps: list[StepRecord] = field(default_factory=list)
    tool_events: list[ToolEvent] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
