"""Extract machine-observable facts from agent trajectories."""

from .adapters import load_run
from .analyze import analyze_run

__all__ = ["analyze_run", "load_run"]
__version__ = "0.1.0"
