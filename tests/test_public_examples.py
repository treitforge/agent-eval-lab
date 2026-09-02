from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from trajectory_facts.adapters import load_run
from trajectory_facts.analyze import analyze_run
from trajectory_facts.dashboard import build_dashboard

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class PublicExampleTests(unittest.TestCase):
    def test_atif_example_has_one_recorded_recovery(self) -> None:
        path = REPOSITORY_ROOT / "examples" / "trajectories" / "atif-toy.json"

        report = analyze_run(load_run(path))

        self.assertEqual(report["run_counts"]["explicit_failed_results"], 1)
        self.assertEqual(report["run_counts"]["explicit_success_results"], 1)
        self.assertEqual(report["run_counts"]["failure_then_success_same_call_groups"], 1)

    def test_sample_harbor_job_builds_two_trial_dashboard(self) -> None:
        job = REPOSITORY_ROOT / "examples" / "sample-harbor-job"
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)

            dashboard = build_dashboard(job, output)

            comparison = json.loads((output / "comparison.json").read_text(encoding="utf-8"))
            self.assertTrue(dashboard.is_file())
            self.assertEqual(comparison["trial_count"], 2)
            self.assertEqual(
                [trial["verifier_rewards"] for trial in comparison["trials"]],
                [{"reward": 1.0}, {"reward": 1.0}],
            )

    def test_toy_public_tests_pass_and_verifier_detects_baseline_defect(self) -> None:
        task = REPOSITORY_ROOT / "examples" / "harbor-toy-task"
        codebase = task / "environment" / "codebase"
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(codebase / "src")

        public_result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(codebase / "tests"),
                "-v",
            ],
            cwd=codebase,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        verifier_result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(task / "tests"),
                "-p",
                "test_*.py",
                "-v",
            ],
            cwd=codebase,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(public_result.returncode, 0, public_result.stderr)
        self.assertNotEqual(verifier_result.returncode, 0)
        self.assertIn("FAILED", verifier_result.stderr)


if __name__ == "__main__":
    unittest.main()
