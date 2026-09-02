"""Command-line interface for trajectory-facts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .adapters import TrajectoryFormatError, load_run
from .analyze import analyze_run
from .render import render_markdown

FORMATS = (
    "auto",
    "atif",
    "otlp-json",
    "swe-agent-traj",
    "mini-swe-agent",
    "native-chat",
    "native-jsonl",
    "openhands-events",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trajectory-facts",
        description="Extract factual evidence from an agent trajectory without ratings.",
    )
    parser.add_argument("trajectory", help="Path to a JSON, JSONL, or .traj file")
    parser.add_argument("--format", choices=FORMATS, default="auto")
    parser.add_argument("--patch", help="Optional unified diff to summarize")
    parser.add_argument("--json-output", help="Write the normalized JSON report")
    parser.add_argument("--markdown-output", help="Write the Markdown report")
    return parser


def _write_output(path_value: str, content: str) -> None:
    path = Path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run = load_run(args.trajectory, args.format)
        report = analyze_run(run, args.patch)
    except (OSError, TrajectoryFormatError, ValueError) as error:
        print(f"trajectory-facts: {error}", file=sys.stderr)
        return 2

    markdown = render_markdown(report)
    try:
        if args.json_output:
            _write_output(
                args.json_output,
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            )
        if args.markdown_output:
            _write_output(args.markdown_output, markdown)
    except OSError as error:
        print(f"trajectory-facts: {error}", file=sys.stderr)
        return 2
    if not args.json_output and not args.markdown_output:
        print(markdown, end="")
    return 0
