#!/usr/bin/env python3
"""Entry point. No install needed: python vam.py <command>."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from vero_monitor.cli import main

if __name__ == "__main__":
    sys.exit(main())
