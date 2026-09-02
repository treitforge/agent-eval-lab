from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from trajectory_facts.dashboard import build_dashboard

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class DashboardTests(unittest.TestCase):
    def test_builds_fact_only_harbor_job_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            job = root / "example-job"
            trial = job / "trial-1"
            (trial / "agent").mkdir(parents=True)
            (trial / "artifacts").mkdir()
            (trial / "verifier").mkdir()
            trajectory = {
                "schema_version": "ATIF-v1.8",
                "session_id": "session-1",
                "agent": {
                    "name": "codex",
                    "version": "1",
                    "model_name": "gpt-test",
                },
                "steps": [
                    {
                        "step_id": 1,
                        "source": "user",
                        "timestamp": "2026-09-01T00:00:00Z",
                        "message": "Run the tests.",
                    },
                    {
                        "step_id": 2,
                        "source": "agent",
                        "timestamp": "2026-09-01T00:00:03Z",
                        "message": "Tests pass.",
                    },
                ],
            }
            (trial / "agent" / "trajectory.json").write_text(
                json.dumps(trajectory), encoding="utf-8"
            )
            (trial / "result.json").write_text(
                json.dumps(
                    {
                        "trial_name": "trial-1",
                        "task_name": "public/example",
                        "started_at": "2026-09-01T00:00:00Z",
                        "finished_at": "2026-09-01T00:00:05Z",
                        "agent_info": {
                            "name": "codex",
                            "version": "1",
                            "model_info": {"name": "gpt-test"},
                        },
                        "verifier_result": {"rewards": {"reward": 1.0}},
                    }
                ),
                encoding="utf-8",
            )
            (trial / "config.json").write_text(
                json.dumps(
                    {
                        "agent": {
                            "model_name": "gpt-test",
                            "kwargs": {"reasoning_effort": "medium"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            (trial / "artifacts" / "patch.diff").write_text(
                "diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-old\n+new\n",
                encoding="utf-8",
            )
            (trial / "verifier" / "test-stdout.txt").write_text(
                "10 passed\n", encoding="utf-8"
            )
            output = root / "report"

            dashboard = build_dashboard(job, output)

            self.assertTrue(dashboard.is_file())
            self.assertTrue((output / "comparison.json").is_file())
            self.assertTrue((output / "comparison.md").is_file())
            content = dashboard.read_text(encoding="utf-8")
            self.assertIn("gpt-test", content)
            self.assertIn("No ratings", content)
            self.assertNotIn("winner is", content.lower())
            facts = json.loads((output / "comparison.json").read_text(encoding="utf-8"))
            self.assertEqual(facts["trial_count"], 1)
            self.assertEqual(facts["trials"][0]["verifier_rewards"], {"reward": 1.0})


if __name__ == "__main__":
    unittest.main()
