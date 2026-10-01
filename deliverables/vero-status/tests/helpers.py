"""Shared helpers: run the bundled fake Vero CLI through the real process code."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vero_status import vero  # noqa: E402

FAKE = ROOT / "scripts" / "fake_vero.py"


def fake_run(args, timeout_s, cwd=None):
    """Like vero.run, but 'vero' is the fake script started with this Python."""
    return vero.run([sys.executable, str(FAKE), *args[1:]], timeout_s, cwd)


def fake_settings(**over):
    from vero_status.settings import Settings

    return Settings(vero_path=sys.executable, **over)
