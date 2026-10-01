"""Shared test helpers. Tests never call the real Vero CLI or Vero Chat."""

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vero_monitor import config  # noqa: E402

FAKE = ROOT / "scripts" / "fake_vero.py"
FIXTURES = ROOT / "tests" / "fixtures"


def make_config(data_dir: Path, **over: Any) -> config.Config:
    """A valid config that runs the fake Vero CLI with the current Python."""
    raw: Dict[str, Any] = {
        "vero": {
            "command": sys.executable,
            "version_args": [str(FAKE), "version"],
            "task_args": [str(FAKE), "task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
            "task_timeout_s": 5,
        },
        "thresholds_s": {"task_slow": 3},
        "schedule": {"interval_minutes": 2},
        "data_dir": str(data_dir),
    }
    return config.build(config.merge(raw, over), data_dir / "monitor.json")
