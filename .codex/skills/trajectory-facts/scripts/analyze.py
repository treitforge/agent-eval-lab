"""Run the repository trajectory analyzer without an installation step."""

from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from trajectory_facts.cli import main  # noqa: E402

raise SystemExit(main())
