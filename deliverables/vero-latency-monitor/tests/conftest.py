"""Shared test helpers (works with unittest and pytest)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
FAKE = ROOT / "scripts" / "fake_vero.py"


def demo_config(data_dir, **over):
    from vero_latency import config
    cfg = config._merge(config.DEFAULTS, {
        "cli": {"command": [sys.executable, str(FAKE), "-p", "{prompt}", "--model", "{model}"],
                "version_command": [sys.executable, str(FAKE), "--version"], "timeout_s": 10},
        "models": [{"id": "fake-mini", "label": "mini"}],
        "data_dir": str(data_dir),
    })
    cfg = config._merge(cfg, over)
    config.validate(cfg)
    return cfg
