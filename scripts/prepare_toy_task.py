"""Create an ignored Harbor task snapshot from the public toy fixture."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "harbor-toy-task"
OUTPUT = ROOT / ".runs" / "tasks" / "scan-ledger-batches"


def _remove_output() -> None:
    resolved_root = ROOT.resolve()
    resolved_output = OUTPUT.resolve()
    if resolved_root not in resolved_output.parents or resolved_output.name != (
        "scan-ledger-batches"
    ):
        raise RuntimeError(f"refusing to remove unexpected path: {resolved_output}")
    if resolved_output.exists():
        shutil.rmtree(resolved_output)


def _ignore(_directory: str, names: list[str]) -> set[str]:
    ignored = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
    }
    return set(names) & ignored


def main() -> int:
    _remove_output()
    shutil.copytree(SOURCE, OUTPUT, ignore=_ignore)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
