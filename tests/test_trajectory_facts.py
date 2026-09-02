from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from trajectory_facts import analyze_run, load_run
from trajectory_facts.analyze import summarize_patch
from trajectory_facts.cli import main

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class TrajectoryFactsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_json(self, name: str, value: object) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_atif_counts_explicit_failures_repeats_and_recovery(self) -> None:
        trajectory = {
            "schema_version": "ATIF-v1.8",
            "session_id": "session-1",
            "agent": {"name": "test-agent", "version": "1", "model_name": "test-model"},
            "steps": [
                {
                    "step_id": 1,
                    "source": "user",
                    "timestamp": "2026-01-01T00:00:00Z",
                    "message": "Run the checks.",
                },
                {
                    "step_id": 2,
                    "source": "agent",
                    "timestamp": "2026-01-01T00:00:01Z",
                    "message": "First run.",
                    "tool_calls": [
                        {
                            "tool_call_id": "call-1",
                            "function_name": "bash",
                            "arguments": {"command": "python -m unittest"},
                        }
                    ],
                    "observation": {
                        "results": [
                            {
                                "content": json.dumps(
                                    {"returncode": 1, "output": "FAILED test_example"}
                                )
                            }
                        ]
                    },
                },
                {
                    "step_id": 3,
                    "source": "agent",
                    "timestamp": "2026-01-01T00:00:04Z",
                    "message": "Second run.",
                    "tool_calls": [
                        {
                            "tool_call_id": "call-2",
                            "function_name": "bash",
                            "arguments": {"command": "python -m unittest"},
                        }
                    ],
                    "observation": {
                        "results": [{"content": json.dumps({"returncode": 0, "output": "OK"})}]
                    },
                },
                {
                    "step_id": 4,
                    "source": "agent",
                    "timestamp": "2026-01-01T00:00:05Z",
                    "message": "All checks pass.",
                },
            ],
            "final_metrics": {"total_steps": 4, "total_prompt_tokens": 100},
        }
        path = self.write_json("trajectory.json", trajectory)

        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "atif")
        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)
        self.assertEqual(report["run_counts"]["explicit_success_results"], 1)
        self.assertEqual(report["run_counts"]["exact_repeated_call_groups"], 1)
        self.assertEqual(report["run_counts"]["failure_then_success_same_call_groups"], 1)
        self.assertEqual(report["time"]["elapsed_seconds_from_timestamps"], 5.0)
        self.assertEqual(
            report["axis_evidence"]["final_response_presentation"]["reference"],
            "steps[3] (step 4)",
        )

    def test_swe_agent_traj_adapter(self) -> None:
        path = self.write_json(
            "example.traj",
            {
                "trajectory": [
                    {
                        "response": "Inspect the repository.",
                        "action": "ls",
                        "observation": {"returncode": 0, "output": "src"},
                    }
                ],
                "info": {"model_stats": {"api_calls": 1, "instance_cost": 0.01}},
            },
        )
        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "swe-agent-traj")
        self.assertEqual(report["run_counts"]["tool_calls"], 1)
        self.assertEqual(report["run_counts"]["explicit_success_results"], 1)
        self.assertEqual(report["metrics"]["api_calls"], 1)

    def test_mini_swe_agent_chat_adapter(self) -> None:
        path = self.write_json(
            "mini.json",
            {
                "trajectory_format": "mini-swe-agent-1",
                "messages": [
                    {"role": "user", "content": "Run tests."},
                    {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [
                            {
                                "id": "tool-1",
                                "function": {
                                    "name": "bash",
                                    "arguments": json.dumps({"command": "pytest"}),
                                },
                            }
                        ],
                    },
                    {
                        "role": "tool",
                        "tool_call_id": "tool-1",
                        "content": json.dumps({"returncode": 0, "output": "1 passed"}),
                    },
                ],
            },
        )
        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "mini-swe-agent")
        self.assertEqual(report["run_counts"]["explicit_success_results"], 1)
        self.assertEqual(
            len(report["axis_evidence"]["core_functionality"]["test_and_build_events"]),
            1,
        )

    def test_native_codex_jsonl_adapter(self) -> None:
        path = self.root / "rollout.jsonl"
        entries = [
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "call_id": "call-1",
                    "name": "exec_command",
                    "arguments": json.dumps({"cmd": "pytest"}),
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call_output",
                    "call_id": "call-1",
                    "output": json.dumps({"returncode": 2, "output": "collection error"}),
                },
            },
        ]
        path.write_text("\n".join(json.dumps(item) for item in entries), encoding="utf-8")

        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "native-jsonl")
        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)

    def test_native_codex_item_completed_commands(self) -> None:
        path = self.root / "codex-rollout.jsonl"
        entries = [
            {
                "type": "event_msg",
                "timestamp": "2026-09-01T00:00:01Z",
                "payload": {
                    "type": "item_completed",
                    "item": {
                        "type": "CommandExecution",
                        "id": "exec-1",
                        "command": ["/bin/bash", "-lc", "pytest -q"],
                        "status": "failed",
                        "aggregated_output": "1 failed",
                        "exit_code": 1,
                        "duration": {"secs": 1, "nanos": 250000000},
                    },
                },
            },
            {
                "type": "event_msg",
                "timestamp": "2026-09-01T00:00:03Z",
                "payload": {
                    "type": "item_completed",
                    "item": {
                        "type": "FileChange",
                        "id": "edit-1",
                        "changes": {"/app/example.py": {"type": "update"}},
                    },
                },
            },
            {
                "type": "response_item",
                "timestamp": "2026-09-01T00:00:04Z",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "Text", "text": "Done."}],
                },
            },
            {
                "type": "event_msg",
                "timestamp": "2026-09-01T00:00:05Z",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "total_token_usage": {
                            "input_tokens": 100,
                            "output_tokens": 20,
                            "total_tokens": 120,
                        },
                        "model_context_window": 200000,
                    },
                },
            },
        ]
        path.write_text("\n".join(json.dumps(item) for item in entries), encoding="utf-8")

        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(report["run_counts"]["tool_calls"], 2)
        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)
        self.assertEqual(run.tool_events[0].duration_ms, 1250.0)
        self.assertEqual(report["metrics"]["total_tokens"], 120)
        self.assertEqual(
            report["axis_evidence"]["final_response_presentation"]["character_count"],
            5,
        )

    def test_native_claude_tool_blocks_adapter(self) -> None:
        path = self.write_json(
            "claude.json",
            [
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "tool_use",
                                "id": "tool-1",
                                "name": "Bash",
                                "input": {"command": "ruff check ."},
                            }
                        ],
                    },
                },
                {
                    "type": "user",
                    "message": {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": "tool-1",
                                "is_error": True,
                                "content": "lint failed",
                            }
                        ],
                    },
                },
            ],
        )
        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "native-jsonl")
        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)
        self.assertEqual(len(report["axis_evidence"]["coding_style"]["style_tool_events"]), 1)

    def test_openhands_event_adapter_pairs_cause_and_action(self) -> None:
        path = self.write_json(
            "openhands.json",
            {
                "events": [
                    {
                        "id": 10,
                        "source": "agent",
                        "action": "run",
                        "args": {"command": "pytest"},
                    },
                    {
                        "id": 11,
                        "source": "environment",
                        "cause": 10,
                        "observation": "command_output",
                        "returncode": 0,
                        "content": "1 passed",
                    },
                ]
            },
        )
        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "openhands-events")
        self.assertEqual(report["run_counts"]["tool_calls"], 1)
        self.assertEqual(report["run_counts"]["explicit_success_results"], 1)

    def test_otlp_json_adapter_uses_explicit_error_status_and_duration(self) -> None:
        path = self.write_json(
            "traces.json",
            {
                "resourceSpans": [
                    {
                        "resource": {
                            "attributes": [
                                {
                                    "key": "gen_ai.agent.name",
                                    "value": {"stringValue": "otel-agent"},
                                }
                            ]
                        },
                        "scopeSpans": [
                            {
                                "scope": {},
                                "spans": [
                                    {
                                        "spanId": "01",
                                        "name": "execute_tool",
                                        "startTimeUnixNano": "1000000000",
                                        "endTimeUnixNano": "1250000000",
                                        "attributes": [
                                            {
                                                "key": "gen_ai.tool.name",
                                                "value": {"stringValue": "shell"},
                                            }
                                        ],
                                        "status": {"code": 2, "message": "failed"},
                                    }
                                ],
                            }
                        ],
                    }
                ]
            },
        )
        run = load_run(path)
        report = analyze_run(run)

        self.assertEqual(run.format_name, "otlp-json")
        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)
        self.assertEqual(report["time"]["sum_explicit_tool_duration_ms"], 250.0)
        self.assertEqual(report["metrics"]["trace_elapsed_seconds"], 0.25)

    def test_patch_summary(self) -> None:
        patch = self.root / "patch.diff"
        patch.write_text(
            """diff --git a/src/a.py b/src/a.py
--- a/src/a.py
+++ b/src/a.py
@@ -1 +1,2 @@
-old
+new
+line
""",
            encoding="utf-8",
        )
        summary = summarize_patch(patch)

        self.assertEqual(summary["files_changed"], 1)
        self.assertEqual(summary["additions"], 2)
        self.assertEqual(summary["deletions"], 1)
        self.assertEqual(summary["hunks"], 1)

    def test_cli_creates_output_parent_directories(self) -> None:
        path = self.write_json(
            "minimal.json",
            {
                "schema_version": "ATIF-v1.8",
                "agent": {"name": "test-agent"},
                "steps": [],
            },
        )
        json_output = self.root / "nested" / "facts.json"
        markdown_output = self.root / "nested" / "facts.md"

        result = main(
            [
                str(path),
                "--json-output",
                str(json_output),
                "--markdown-output",
                str(markdown_output),
            ]
        )

        self.assertEqual(result, 0)
        self.assertTrue(json_output.is_file())
        self.assertTrue(markdown_output.is_file())


if __name__ == "__main__":
    unittest.main()
