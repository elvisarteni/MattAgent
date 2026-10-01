"""Double-click to open the Vero Status dashboard (no console window)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vero_status.app import run  # noqa: E402

run()
